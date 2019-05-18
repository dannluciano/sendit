import os
import logging
import logging.handlers
import shlex
import subprocess

tmp_dir = "temp"


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


log_file_path = "temp/submission_runner.log"
log = logging.getLogger("SubmissionRunner")
log.addHandler(
    logging.handlers.RotatingFileHandler(log_file_path, maxBytes=1024 * 1024)
)
log.setLevel(20)


class SubmissionRunner(object):
    def __init__(
        self, work_dir, input_content, expected_output_content, source_file_content
    ):
        self.compiler_command = "echo compiler"
        self.executable_command = "echo executable"
        self.source_file_name = "source.txt"
        self.timeout = 5

        self.work_dir = f"{tmp_dir}/{work_dir}"
        self.input_content = input_content
        self.expected_output_content = expected_output_content
        self.source_file_content = source_file_content

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
            self.work_dir, "expected_output.txt", self.expected_output_content
        )
        self.create_temp_file(
            self.work_dir, self.source_file_name, self.source_file_content
        )

    def run_process(self, command):
        try:
            log.info(f"Spawn Process: timeout {self.timeout} {command}")
            subprocess.run(
                f"exec {command}", shell=True, check=True, timeout=self.timeout
            )
        except subprocess.TimeoutExpired as error:
            log.error(f"Timeout Error: {command}")
            raise SubmissionTimeoutError("TimeoutError")

    def run_compiler(self):
        log.info(f"Executing Compiler: {self.compiler_command}")
        try:
            self.run_process(self.compiler_command)
        except subprocess.CalledProcessError as error:
            log.error(f"Sintax Error: {error.stderr}")
            raise SubmissionSintaxError("SintaxError")

    def run_executable(self):
        log.info(f"Executing Program: {self.executable_command}")
        try:
            self.run_process(self.executable_command)
        except subprocess.CalledProcessError as error:
            log.error(f"Runtime Error: {error.stderr}")
            raise SubmissionRuntimeError("RuntimeError")

    def compare_outputs(self):
        command = f"diff -E -b -w -B {self.work_dir}/expected_output.txt {self.work_dir}/computed_output.txt > {self.work_dir}/diff.out.txt 2> {self.work_dir}/diff.err.txt"
        log.info(f"Executing Diff: {command}")
        try:
            self.run_process(command)
        except subprocess.CalledProcessError as error:
            log.error(f"Diff Error: {error.stderr}")
            raise SubmissionDiffError("DiffError")

    def run(self):
        log.info("-" * 80)
        log.info("Submission Runner Started")
        self.create_temp_dirs_and_files()
        try:
            self.run_compiler()
            self.run_executable()
            self.compare_outputs()
        except SubmissionError as error:
            log.info(error.message)
            return error.message
        log.info("OK")
        return "OK"


class C_SubmissionRunner(SubmissionRunner):
    def __init__(
        self, work_dir, input_content, expected_output_content, source_file_content
    ):
        super().__init__(
            work_dir, input_content, expected_output_content, source_file_content
        )
        self.source_file_name = "main.c"
        self.compiler_command = f"gcc -o {self.work_dir}/main {self.work_dir}/{self.source_file_name} > {self.work_dir}/compiler.out.txt 2> {self.work_dir}/compiler.err.txt"
        self.executable_command = f"{self.work_dir}/main < {self.work_dir}/input.txt > {self.work_dir}/computed_output.txt 2> {self.work_dir}/stderr.txt"


class Cplusplus11_SubmissionRunner(SubmissionRunner):
    def __init__(
        self, work_dir, input_content, expected_output_content, source_file_content
    ):
        super().__init__(
            work_dir, input_content, expected_output_content, source_file_content
        )
        self.source_file_name = "main.c"
        self.compiler_command = f"g++ --std=c++11 -o {self.work_dir}/main {self.work_dir}/{self.source_file_name} > {self.work_dir}/compiler.out.txt 2> {self.work_dir}/compiler.err.txt"
        self.executable_command = f"{self.work_dir}/main < {self.work_dir}/input.txt > {self.work_dir}/computed_output.txt 2> {self.work_dir}/stderr.txt"


class JavaScript_SubmissionRunner(SubmissionRunner):
    def __init__(
        self, work_dir, input_content, expected_output_content, source_file_content
    ):
        super().__init__(
            work_dir, input_content, expected_output_content, source_file_content
        )
        self.source_file_name = "index.js"
        self.compiler_command = f"nodejs -c {self.work_dir}/{self.source_file_name} > {self.work_dir}/compiler.out.txt 2> {self.work_dir}/compiler.err.txt"
        self.executable_command = f"nodejs {self.work_dir}/main.js < {self.work_dir}/input.txt > {self.work_dir}/computed_output.txt 2> {self.work_dir}/stderr.txt"

    def run_executable(self):
        self.run_process(
            f"cat browser_io.js {self.work_dir}/{self.source_file_name} > {self.work_dir}/main.js"
        )
        super().run_executable()


class JAVA_SubmissionRunner(SubmissionRunner):
    def __init__(
        self, work_dir, input_content, expected_output_content, source_file_content
    ):
        super().__init__(
            work_dir, input_content, expected_output_content, source_file_content
        )
        self.source_file_name = "Principal.java"
        self.compiler_command = f"javac {self.work_dir}/{self.source_file_name} > {self.work_dir}/compiler.out.txt 2> {self.work_dir}/compiler.err.txt"
        self.executable_command = f"java -cp {self.work_dir} Principal < {self.work_dir}/input.txt > {self.work_dir}/computed_output.txt 2> {self.work_dir}/stderr.txt"
        self.timeout = 3


class Python_SubmissionRunner(SubmissionRunner):
    def __init__(
        self, work_dir, input_content, expected_output_content, source_file_content
    ):
        super().__init__(
            work_dir, input_content, expected_output_content, source_file_content
        )
        self.source_file_name = "main.py"
        self.compiler_command = f"python -m py_compile {self.work_dir}/{self.source_file_name} > {self.work_dir}/compiler.out.txt 2> {self.work_dir}/compiler.err.txt"
        self.executable_command = f"python {self.work_dir}/{self.source_file_name} < {self.work_dir}/input.txt > {self.work_dir}/computed_output.txt 2> {self.work_dir}/stderr.txt"


class SubmissionRunnerManager:
    @staticmethod
    def exe(
        lang, work_dir, input_content, expected_output_content, source_file_content
    ):
        runners = {
            "c": C_SubmissionRunner,
            "c++11": Cplusplus11_SubmissionRunner,
            "javascript": JavaScript_SubmissionRunner,
            "java": JAVA_SubmissionRunner,
            "python": Python_SubmissionRunner,
        }
        return runners[lang](
            work_dir, input_content, expected_output_content, source_file_content
        ).run()
