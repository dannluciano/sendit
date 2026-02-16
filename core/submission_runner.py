import io
import logging
import logging.handlers
import os
import uuid

import docker

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
        self.compiler_command = "echo compiler"
        self.executable_command = "echo executable"
        self.source_file_name = "source.txt"
        self.timeout = 8

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
        container_name = str(uuid.uuid4())

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
                stdin_open=True,
                mem_limit="512m",
                nano_cpus=2_000_000_000,
                network_mode="none",
                pids_limit=64,
                # security_opt=["no-new-privileges"],
                # read_only=True,
                # cap_drop=["ALL"],
                detach=True,
            )

            result = container.wait(timeout=self.timeout)
            logs = container.logs(stdout=True, stderr=True)

            self.last_output = logs.decode("utf-8")[:1000]

            exit_code = result["StatusCode"]

            container.remove(force=True)

            if exit_code != 0:
                raise SubmissionRuntimeError("Execution failed")

        except docker.errors.APIError as e:
            raise SubmissionRuntimeError(f"Docker API Error: {str(e)}")

        except Exception as e:
            log.error(e)
            raise SubmissionTimeoutError("TimeoutError")

    def run_compiler(self):
        try:
            self.run_process(self.compiler_image, self.compiler_cmd)
        except Exception as e:
            log.error(e)
            raise SubmissionSintaxError("SintaxError")

    def run_executable(self):
        try:
            self.run_process(
                self.executable_image, self.executable_cmd, self.input_content
            )
        except Exception:
            raise SubmissionRuntimeError("RuntimeError")

    def compare_outputs(self):
        self.create_temp_file(
            self.work_dir, "expected_output.txt", self.expected_output_content
        )
        command = f"diff -u -b -w -B - {self.work_dir}/expected_output.txt"
        log.info(f"Executing Diff: {command}")
        try:
            self.run_process(command, self.last_output)
        except subprocess.CalledProcessError as error:
            self.last_output = error.stdout
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
            return {
                "status": error.message,
                "output": str(self.last_output) + "\n" + error.message,
            }
        finally:
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
        self.compiler_image = "gcc:15"
        self.compiler_cmd = f"gcc -o main {self.source_file_name}"
        self.executable_image = "gcc:15"
        self.executable_cmd = "./main"


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
        self.compiler_command = f"{self.docker_start_command} gcc:15 g++ --std=c++11 -o main {self.source_file_name}"
        self.executable_command = f"{self.docker_start_command} gcc:15 ./main"


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
        self.compiler_command = f"{self.docker_start_command} node:24.13.1-alpine node -c {self.source_file_name}"
        self.executable_command = f"{self.docker_start_command} node:24.13.1-alpine node {self.source_file_name}"


class JAVA_SubmissionRunner(SubmissionRunner):
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
        self.compiler_command = f"{self.docker_start_command} eclipse-temurin:21 javac {self.source_file_name}"
        self.executable_command = f"{self.docker_start_command} eclipse-temurin:21 java -cp . Principal"
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
        self.compiler_image = "python:3.14-alpine"
        self.compiler_cmd = f"python -m py_compile {self.source_file_name}"
        self.executable_image = "python:3.14-alpine"
        self.executable_cmd = f"python {self.source_file_name}"


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
            "java": JAVA_SubmissionRunner,
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
