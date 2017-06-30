import subprocess
import tempfile
import logging
import os
import shlex
import time
import difflib


class JSSintaxError(Exception):
    pass


class JSRuntimeError(Exception):
    pass


class JSTimeoutError(Exception):
    pass


class JSNoInputError(Exception):
    pass


class DiffError(Exception):
    pass


L = logging.getLogger('SubmissionRunner')
L.addHandler(logging.FileHandler('submission_runner.log'))
L.setLevel(logging.INFO)

with open('browser_io.js') as browser_io_file:
    browser_io_code = browser_io_file.read()


def run_submission(code='', expected_input='', expected_output=''):
    L.info('SubmissionRunner Started...')
    with tempfile.TemporaryDirectory() as tmp_dir:
        L.info(f'Created Temporary Dir: {tmp_dir}')

        os.chdir(tmp_dir)
        pwd = os.getcwd()
        L.info(f'Changed Working Dir: {pwd}')

        code = f"""
        {browser_io_code}
        {code}
        """

        code_file = tempfile.NamedTemporaryFile(
            'w+', dir=tmp_dir, delete=False, prefix='code_', suffix='.js')
        code_file.write(code)
        code_file.seek(0)
        L.info(f'Created Temporary File: {code_file.name}')
        L.debug(code_file.read())

        input_file = tempfile.NamedTemporaryFile(
            'w+', dir=tmp_dir, delete=False, prefix='input_', suffix='.txt')
        input_file.write(expected_input)
        input_file.seek(0)
        L.info(f'Created Temporary File: {input_file.name}')
        L.debug(input_file.read())
        input_file.seek(0)

        output_file = tempfile.NamedTemporaryFile(
            'w+', dir=tmp_dir, delete=False, prefix='output_', suffix='.txt')
        output_file.write(expected_output)
        output_file.seek(0)
        L.info(f'Created Temporary File: {output_file.name}')
        L.debug(output_file.read())

        node_command = f'node -i {code_file.name}'

        L.info(f'Executing Node Command: {node_command}')
        try:
            if (expected_input != ''):
                process = subprocess.Popen(
                    shlex.split(node_command),
                    stdout=subprocess.PIPE,
                    stderr=subprocess.PIPE,
                    stdin=subprocess.PIPE)

                outs, errs = process.communicate(
                    input=expected_input.encode(),
                    timeout=1)
            else:
                process = subprocess.run(
                    shlex.split(node_command),
                    stdout=subprocess.PIPE,
                    stderr=subprocess.PIPE,
                    check=True, timeout=1)

                outs = process.stdout
                errs = process.stderr

        except subprocess.TimeoutExpired as error:
            L.error(f'Timeout Error:')
            raise JSTimeoutError('Timeout Error')
        except subprocess.CalledProcessError as error:
            if b'SyntaxError:' in error.stderr:
                L.error(f'SintaxError: ')
                raise JSSintaxError('SintaxError')
            else:
                L.error(f'RuntimeError: ')
                raise JSRuntimeError('RuntimeError')

        result_file = tempfile.NamedTemporaryFile(
            'w+', dir=tmp_dir, delete=False, prefix='result_', suffix='.txt')
        result_file.write(outs.decode('utf8'))
        result_file.seek(0)
        L.info(f'Created Temporary File: {result_file.name}')
        L.debug(result_file.read())

        diff_command = f'diff -E -b -w -B {output_file.name} {result_file.name}'
        L.info(f'Executing Diff Command: {diff_command}')
        try:
            process = subprocess.run(
                shlex.split(diff_command),
                stdout=subprocess.PIPE, stderr=subprocess.PIPE,
                check=True)
        except subprocess.CalledProcessError as error:
            L.error('Diff Error: Expected Output != Computed Output')
            L.debug(error.stdout.decode('utf8'))
            raise DiffError('Expected Output != Computed Output')

        L.info('-------------------------------------------------------------')
        return True
