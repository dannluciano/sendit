import subprocess
import tempfile
import logging
import os
import shlex
import shutil

from django.conf import settings


L = logging.getLogger('SubmissionRunner')

settings.configure(DEBUG=True, BASE_DIR=os.getcwd())

log_file_path = 'temp/submission_runner.log'
if settings.DEBUG:
    L.addHandler(logging.FileHandler(log_file_path))
    L.setLevel(logging.DEBUG)
else:
    L.addHandler(logging.handlers.RotatingFileHandler(
        log_file_path,
        maxBytes=1024 * 1024))


def create_temp_file(content, prefix='', suffix='.txt'):
    filename = '{}{}'.format(prefix, suffix)
    file = open(filename, 'w+')
    file.write(content)
    file.seek(0)
    L.info(f'Created Temporary File: {file.name}')
    L.debug(file.read())
    return file


def run_submission(id=0, code='', input='', expected_output=''):
    L.info('SubmissionRunner Started...')
    result = 'OK'
    
    tmp_dir = 'temp/submission_{}'.format(id)
    try:
        os.chdir(tmp_dir)
    except FileNotFoundError as e:
        os.mkdir(tmp_dir)
        os.chdir(tmp_dir)
    
    pwd = os.getcwd()
    L.info(f'Created Temporary Changed Working Dir: {pwd}')

    code_file = create_temp_file(code, 'Principal', '.java')

    input_file = create_temp_file(
        input, 'input', '.txt')

    output_file = create_temp_file(
        expected_output, 'output', '.txt')

    command = f'javac {code_file.name}'

    L.info(f'Executing Command: {command}')
    process = subprocess.run(shlex.split(command))

    command = f'java Principal'

    L.info(f'Executing Command: {command}')
    outs = b''
    try:
        if input != '':
            process = subprocess.Popen(
                shlex.split(command),
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
                stdin=subprocess.PIPE)

            outs, errs = process.communicate(
                input=input.encode(),
                timeout=1)
        else:
            process = subprocess.run(
                shlex.split(command),
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
                check=True, timeout=1)

            outs = process.stdout
            errs = process.stderr

    except subprocess.TimeoutExpired as error:
        result = 'JSTimeoutError'
        L.error('Timeout Error:')
    except subprocess.CalledProcessError as error:
        result = 'JSSintaxError'
        L.error('SintaxError: ')

    result_file = create_temp_file(
        outs.decode('utf8'), 'result', '.txt')

    if result == 'OK':
        diff_command = f'diff -E -b -w -B {output_file.name} {result_file.name}'
        L.info(f'Executing Diff Command: {diff_command}')
        try:
            subprocess.run(
                shlex.split(diff_command), stdout=subprocess.PIPE, check=True)
        except subprocess.CalledProcessError as error:
            result = 'DiffError'
            L.error('Diff Error: Expected Output != Computed Output')
            L.debug(error.stdout.decode('utf8'))
            L.debug(outs.decode('utf8'))
    
    os.chdir(settings.BASE_DIR)
    if not settings.DEBUG:
        rmtree(temp_dir_name)

    L.info('-' * 80)
    return result


if __name__ == "__main__":
    code = """
class Principal {
    public static void main(String args[]) {
        System.out.println("Ola Mundo");
    }
}
"""
    input = """"""
    expected_output = """Ola Mundo"""

    print(run_submission(id=1, code=code, input=input, expected_output=expected_output))


    code = """
class Principal {
    public static void main(String args[]) {
        while(true){

        }
    }
}
"""
    input = """"""
    expected_output = """Ola Mundo"""

    print(run_submission(id=2, code=code, input=input, expected_output=expected_output))

    code = """
class Principal {
    public static void main(String args[]) {
        System.out.println("Ola Mundo")
    }
}
"""
    input = """"""
    expected_output = """Ola Mundo"""

    print(run_submission(id=3, code=code, input=input, expected_output=expected_output))

    code = """
import java.util.Scanner;    
class Principal {
    public static void main(String args[]) {
        Scanner scanner = null;
        int i = scanner.nextInt();
    }
}
"""
    input = """"""
    expected_output = """Ola Mundo"""

    print(run_submission(id=4, code=code, input=input, expected_output=expected_output))

    code = """
class Principal {
    public static void main(String args[]) {
        System.out.println("Oi");
    }
}
"""
    input = """"""
    expected_output = """Ola Mundo"""

    print(run_submission(id=5, code=code, input=input, expected_output=expected_output))