import difflib
import io
import logging
import logging.handlers
import os
import shutil

import docker
from requests.exceptions import ReadTimeout
from urllib3.exceptions import ReadTimeoutError

IMAGE_VERSION_DICT = {
    "c": "gcc:15",
    "cplusplus": "gcc:15",
    "javascript": "node:24.13.1-alpine",
    "java": "eclipse-temurin:21",
    "python": "python:3.14-alpine",
}

log = logging.getLogger("SubmissionRunner")
log.setLevel(logging.INFO)

log_capture_string = io.StringIO()
log.addHandler(logging.StreamHandler(log_capture_string))

tmp_dir = "/temp"

if not os.path.exists(tmp_dir):
    os.makedirs(tmp_dir)


class SubmissionError(Exception):
    def __init__(self, message):
        self.message = message


class SubmissionSintaxError(SubmissionError):
    pass


class SubmissionRuntimeError(SubmissionError):
    pass


class SubmissionTimeoutError(SubmissionError):
    pass


class SubmissionDiffError(SubmissionError):
    pass


class SubmissionRunner(object):
    def __init__(
        self,
        work_dir_name,
        input_content,
        expected_output_content,
        source_file_content,
    ):
        self.image_name = "hello-world"
        self.compiler_command = "echo compiler"
        self.executable_command = "echo executable"
        self.source_file_name = "source.txt"
        self.timeout = 4

        self.work_dir_name = work_dir_name
        self.work_dir = f"{tmp_dir}/{self.work_dir_name}"
        self.input_content = input_content.replace("\r", "")
        self.expected_output_content = expected_output_content
        self.source_file_content = source_file_content
        self.last_output = ""
        self.client = docker.from_env()

    def create_temp_file(self, dirname, filename, content):
        file_path = f"{dirname}/{filename}"
        with open(file_path, "w+") as file:
            file.write(content)
            log.info(f"Created Temporary File: {file.name}")
        return

    def create_temp_dir(self, dirname):
        os.makedirs(dirname, exist_ok=True)
        log.info(f"Created Temporary Directory: {dirname}")

    def destroy_temp_dir(self, path):
        shutil.rmtree(path, ignore_errors=True)
        log.info(f"Destroyed Temporary Directory: {path}")

    def create_temp_dirs_and_files(self):
        self.create_temp_dir(self.work_dir)
        self.create_temp_file(self.work_dir, "input.txt", self.input_content)
        self.create_temp_file(
            self.work_dir, self.source_file_name, self.source_file_content
        )

    def create_container(self):
        pass

    def destroy_container(self):
        pass

    def run_process(self, image, command, input_=None):
        container_name = f"c_{self.work_dir_name}"
        container = None
        try:
            container = self.client.containers.run(
                image=image,
                name=container_name,
                command=command,
                volumes={
                    "temp": {
                        "bind": "/app",
                        "mode": "rw",
                    }
                },
                working_dir=f"/app/{self.work_dir_name}",
                mem_limit="512m",
                nano_cpus=2_000_000_000,
                network_mode="none",
                pids_limit=64,
                security_opt=["no-new-privileges"],
                read_only=True,
                cap_drop=["ALL"],
                detach=True,
            )

            try:
                result = container.wait(timeout=self.timeout)
            except (ReadTimeout, ReadTimeoutError):
                container.kill()
                raise SubmissionTimeoutError("TimeoutError")

            except Exception as e:
                if "Read timed out" in str(e):
                    container.kill()
                    raise SubmissionTimeoutError("TimeoutError")
                else:
                    raise

            exit_code = result["StatusCode"]

            logs = container.logs(stdout=True, stderr=True)
            self.last_output = logs.decode("utf-8")[:10000]

            if exit_code != 0:
                raise SubmissionRuntimeError("RuntimeError")

        except docker.errors.APIError as e:
            raise SubmissionRuntimeError(f"Docker API Error: {str(e)}")

        except SubmissionError:
            raise

        except Exception as e:
            raise SubmissionRuntimeError(f"UnexpectedError: {str(e)}")

        finally:
            if container:
                try:
                    container.remove(force=True)
                except:
                    pass

    def run_compiler(self):
        try:
            self.run_process(self.image_name, self.compiler_command)
        except Exception as e:
            log.error(e)
            raise SubmissionSintaxError("SintaxError")

    def run_executable(self):
        try:
            self.run_process(
                self.image_name,
                self.executable_command,
                self.input_content,
            )

        except Exception as e:
            log.error(e)
            raise

    def compare_outputs(self):
        diff = list(
            difflib.unified_diff(
                self.expected_output_content.splitlines(),
                self.last_output.splitlines(),
                fromfile="expected",
                tofile="actual",
                lineterm="",
            )
        )

        if diff:
            self.last_output = "\n".join(diff) if diff else ""
            raise SubmissionDiffError("DiffError")

    def run(self):
        log.info("-" * 80)
        self.create_container()
        self.create_temp_dirs_and_files()
        try:
            self.run_compiler()
            self.run_executable()
            if self.expected_output_content:
                self.compare_outputs()
        except SubmissionError as error:
            log.info(error.message)
            output_text = str(self.last_output) if self.last_output else ""
            return {
                "status": error.message,
                "output": output_text + "\n" + error.message,
            }

        except Exception as e:
            return {
                "status": "InternalError",
                "output": str(e),
            }
        finally:
            self.destroy_temp_dir(self.work_dir)
            self.destroy_container()
        log.info("OK")
        return {"status": "OK", "output": self.last_output}


class C_SubmissionRunner(SubmissionRunner):
    def __init__(
        self,
        work_dir,
        input_content,
        expected_output_content,
        source_file_content,
    ):
        super().__init__(
            work_dir,
            input_content,
            expected_output_content,
            source_file_content,
        )
        self.source_file_name = "main.c"
        self.image_name = IMAGE_VERSION_DICT["c"]
        self.compiler_command = f"gcc -o main {self.source_file_name}"
        self.executable_command = "sh -c './main < input.txt'"


class Cplusplus_SubmissionRunner(SubmissionRunner):
    def __init__(
        self,
        work_dir,
        input_content,
        expected_output_content,
        source_file_content,
    ):
        super().__init__(
            work_dir,
            input_content,
            expected_output_content,
            source_file_content,
        )
        self.source_file_name = "main.cpp"
        self.image_name = IMAGE_VERSION_DICT["cplusplus"]
        self.compiler_command = f"g++ -o main {self.source_file_name}"
        self.executable_command = "sh -c './main < input.txt'"


class JavaScript_SubmissionRunner(SubmissionRunner):
    def __init__(
        self,
        work_dir,
        input_content,
        expected_output_content,
        source_file_content,
    ):
        iof = open("browser_io.js", mode="r")
        ioc = iof.read()
        iof.close()
        source_file_content = f"{ioc}\n{source_file_content}"
        super().__init__(
            work_dir,
            input_content,
            expected_output_content,
            source_file_content,
        )
        self.source_file_name = "index.js"
        self.image_name = IMAGE_VERSION_DICT["javascript"]
        self.compiler_command = f"node -c {self.source_file_name}"
        self.executable_command = (
            f"sh -c 'node {self.source_file_name} < input.txt'"
        )


class Java_SubmissionRunner(SubmissionRunner):
    def __init__(
        self,
        work_dir,
        input_content,
        expected_output_content,
        source_file_content,
    ):
        super().__init__(
            work_dir,
            input_content,
            expected_output_content,
            source_file_content,
        )
        self.source_file_name = "Principal.java"
        self.image_name = IMAGE_VERSION_DICT["java"]
        self.compiler_command = f"javac {self.source_file_name}"
        self.executable_command = "sh -c 'java -cp . Principal < input.txt'"

        self.timeout = self.timeout + 2


class Python_SubmissionRunner(SubmissionRunner):
    def __init__(
        self,
        work_dir,
        input_content,
        expected_output_content,
        source_file_content,
    ):
        super().__init__(
            work_dir,
            input_content,
            expected_output_content,
            source_file_content,
        )
        self.source_file_name = "main.py"
        self.image_name = IMAGE_VERSION_DICT["python"]
        self.compiler_command = (
            f"python -m py_compile {self.source_file_name}"
        )
        self.executable_command = (
            f"sh -c 'python {self.source_file_name} < input.txt'"
        )


class SubmissionRunnerManager:
    @staticmethod
    def exe(
        lang,
        work_dir,
        input_content,
        expected_output_content,
        source_file_content,
    ):
        runners = {
            "c": C_SubmissionRunner,
            "cplusplus": Cplusplus_SubmissionRunner,
            "javascript": JavaScript_SubmissionRunner,
            "java": Java_SubmissionRunner,
            "python": Python_SubmissionRunner,
        }

        result = runners[lang](
            work_dir,
            input_content,
            expected_output_content,
            source_file_content,
        ).run()

        log_contents = log_capture_string.getvalue()
        return {
            "status": result["status"],
            "output": result["output"],
            "log": log_contents,
        }
