import io
import logging
import logging.handlers
import os
import shlex
import subprocess
import uuid

from django.conf import settings

log = logging.getLogger("SubmissionRunner")
log.setLevel(logging.INFO)

log_capture_string = io.StringIO()
log.addHandler(logging.StreamHandler(log_capture_string))

tmp_dir = "temp"

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
        self, work_dir_name, input_content, expected_output_content, source_file_content
    ):
        self.compiler_command = "echo compiler"
        self.executable_command = "echo executable"
        self.source_file_name = "source.txt"
        self.timeout = 4

        self.work_dir = f"{tmp_dir}/{work_dir_name}"
        self.input_content = input_content.replace("\r", "")
        self.expected_output_content = expected_output_content
        self.source_file_content = source_file_content
        self.last_output = ""
        self.docker_start_command = f"docker run -i --rm --cpus=1 --memory 512MB --name $NAME$ -v {settings.BASE_DIR}/{self.work_dir}:/app -w /app"
        self.docker_stop_command = "docker kill $NAME$"

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
        if self.expected_output_content:
            self.create_temp_file(
                self.work_dir, "expected_output.txt", self.expected_output_content
            )
        self.create_temp_file(
            self.work_dir, self.source_file_name, self.source_file_content
        )

    def run_process(self, command, input_=None):
        try:
            container_name = str(uuid.uuid4())
            command = command.replace("$NAME$", container_name)

            log.info(f"RUNNING: {command}")

            result = subprocess.run(
                shlex.split(command),
                shell=False,
                check=True,
                timeout=self.timeout,
                stdout=subprocess.PIPE,
                stderr=subprocess.STDOUT,
                input=input_,
            )
            self.last_output = result.stdout[0:1000].decode("utf-8")
        except subprocess.TimeoutExpired as error:
            command = self.docker_stop_command.replace("$NAME$", container_name)
            result = subprocess.run(
                shlex.split(command),
                shell=False,
                check=True,
            )

            if error.stdout:
                self.last_output = error.stdout[0:1000]
            else:
                self.last_output = ""
            raise SubmissionTimeoutError("TimeoutError")

    def run_compiler(self):
        log.info(f"Executing Compiler: {self.compiler_command}")
        try:
            self.run_process(self.compiler_command)
        except subprocess.CalledProcessError as error:
            self.last_output = error.stdout.decode("utf-8")
            raise SubmissionSintaxError("SintaxError")

    def run_executable(self):
        log.info(f"Executing Program: {self.executable_command}")
        try:
            self.run_process(self.executable_command, self.input_content.encode())
        except subprocess.CalledProcessError as error:
            self.last_output = error.stdout.decode("utf-8")
            raise SubmissionRuntimeError("RuntimeError")

    def compare_outputs(self):
        command = f"diff -u -b -w -B - {self.work_dir}/expected_output.txt"
        log.info(f"Executing Diff: {command}")
        try:
            self.run_process(command, self.last_output.encode())
        except subprocess.CalledProcessError as error:
            self.last_output = error.stdout.decode("utf-8")
            raise SubmissionDiffError("DiffError")

    def run(self):
        log.info("-" * 80)
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
        log.info("OK")
        return {"status": "OK", "output": self.last_output}


class C_SubmissionRunner(SubmissionRunner):
    def __init__(
        self, work_dir, input_content, expected_output_content, source_file_content
    ):
        super().__init__(
            work_dir, input_content, expected_output_content, source_file_content
        )
        self.source_file_name = "main.c"
        self.compiler_command = (
            f"{self.docker_start_command} gcc:12 gcc -o main {self.source_file_name}"
        )
        self.executable_command = f"{self.docker_start_command} gcc:12 ./main"


class Cplusplus_SubmissionRunner(SubmissionRunner):
    def __init__(
        self, work_dir, input_content, expected_output_content, source_file_content
    ):
        super().__init__(
            work_dir, input_content, expected_output_content, source_file_content
        )
        self.source_file_name = "main.cpp"
        self.compiler_command = f"{self.docker_start_command} gcc:12 g++ --std=c++11 -o main {self.source_file_name}"
        self.executable_command = f"{self.docker_start_command} gcc:12 ./main"


class JavaScript_SubmissionRunner(SubmissionRunner):
    def __init__(
        self, work_dir, input_content, expected_output_content, source_file_content
    ):
        iof = open("browser_io.js", mode="r")
        ioc = iof.read()
        iof.close()
        source_file_content = f"{ioc}\n{source_file_content}"
        super().__init__(
            work_dir, input_content, expected_output_content, source_file_content
        )
        self.source_file_name = "index.js"
        self.compiler_command = f"{self.docker_start_command} node:20.10.0-alpine node -c {self.source_file_name}"
        self.executable_command = f"{self.docker_start_command} node:20.10.0-alpine node {self.source_file_name}"


class JAVA_SubmissionRunner(SubmissionRunner):
    def __init__(
        self, work_dir, input_content, expected_output_content, source_file_content
    ):
        super().__init__(
            work_dir, input_content, expected_output_content, source_file_content
        )
        self.source_file_name = "Principal.java"
        self.compiler_command = f"{self.docker_start_command} eclipse-temurin:11 javac {self.source_file_name}"
        self.executable_command = (
            f"{self.docker_start_command} eclipse-temurin:11 java -cp . Principal"
        )
        self.timeout = 5


class Python_SubmissionRunner(SubmissionRunner):
    def __init__(
        self, work_dir, input_content, expected_output_content, source_file_content
    ):
        super().__init__(
            work_dir, input_content, expected_output_content, source_file_content
        )
        self.source_file_name = "main.py"
        self.compiler_command = f"{self.docker_start_command} python:alpine python -m py_compile {self.source_file_name}"
        self.executable_command = (
            f"{self.docker_start_command} python:alpine python {self.source_file_name}"
        )
        self.worker_env = "./worker_env"


class SubmissionRunnerManager:
    @staticmethod
    def exe(
        lang, work_dir, input_content, expected_output_content, source_file_content
    ):
        runners = {
            "c": C_SubmissionRunner,
            "c++11": Cplusplus_SubmissionRunner,
            "cplusplus": Cplusplus_SubmissionRunner,
            "javascript": JavaScript_SubmissionRunner,
            "java": JAVA_SubmissionRunner,
            "python": Python_SubmissionRunner,
        }

        result = runners[lang](
            work_dir, input_content, expected_output_content, source_file_content
        ).run()

        log_contents = log_capture_string.getvalue()
        return {
            "status": result["status"],
            "output": result["output"],
            "log": log_contents,
        }
