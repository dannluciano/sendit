import subprocess
import tempfile
import logging
import os
import shlex
from django.conf import settings


L = logging.getLogger('SubmissionRunner')
if settings.DEBUG:
    L.addHandler(logging.FileHandler('submission_runner.log'))
    L.setLevel(logging.DEBUG)
else:
    L.addHandler(logging.RotatingFileHandler(
        'submission_runner.log',
        maxBytes=1024 * 1024))


def create_temp_file(content, temp_dir='', prefix='', suffix='.txt'):
    file = tempfile.NamedTemporaryFile(
        'w+', dir=temp_dir, delete=False, prefix=prefix, suffix=suffix)
    file.write(content)
    file.seek(0)
    L.info(f'Created Temporary File: {file.name}')
    L.debug(file.read())
    return file


def run_submission(code='', expected_input='', expected_output=''):
    L.info('SubmissionRunner Started...')
    result = 'OK'
    with tempfile.TemporaryDirectory() as tmp_dir:
        os.chdir(tmp_dir)
        pwd = os.getcwd()
        L.info(f'Created Temporary Changed Working Dir: {pwd}')

        code_file = create_temp_file(code, tmp_dir, 'code_', '.js')

        input_file = create_temp_file(
            expected_input, tmp_dir, 'input_', '.txt')

        output_file = create_temp_file(
            expected_output, tmp_dir, 'output_', '.txt')

        node_command = f'node -i {code_file.name}'

        L.info(f'Executing Node Command: {node_command}')
        outs = b''
        try:
            if expected_input != '':
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
            result = 'JSTimeoutError'
            L.error('Timeout Error:')
        except subprocess.CalledProcessError as error:
            if b'SyntaxError:' in error.stderr:
                result = 'JSSintaxError'
                L.error('SintaxError: ')
            else:
                result = 'JSRuntimeError'
                L.error(f'RuntimeError: ')

        result_file = create_temp_file(
            outs.decode('utf8'), tmp_dir, 'result_', '.txt')

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

    os.chdir(settings.BASE_DIR)
    L.info('-' * 80)
    return result
