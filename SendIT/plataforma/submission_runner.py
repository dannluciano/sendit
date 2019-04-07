import os
import logging
import logging.handlers
import shlex
import subprocess

tmp_dir = 'temp'

class SubmissionError(Exception):
  def __init__(self, message):
    self.message = message

class SintaxError(SubmissionError):
  pass

class RuntimeError(SubmissionError):
  pass

class TimeoutError(SubmissionError):
  pass

class DiffError(SubmissionError):
  pass

log_file_path = 'temp/submission_runner.log'
log = logging.getLogger('SubmissionRunner')
log.addHandler(logging.handlers.RotatingFileHandler(log_file_path, maxBytes=1024 * 1024))
log.setLevel(20)

class SubmissionRunner(object):

  def __init__(self):
    
    self.source_file_name = 'source.txt'

  def create_temp_file(self, dir, filename, content):
    file_path = f'{dir}/{filename}'
    with open(file_path, 'w+') as file:
      file.write(content)
      log.info(f'Created Temporary File: {file.name}')
    return
  
  def create_temp_dir(self, dirname):
    try:
      os.mkdir(dirname)
    except FileExistsError:
      pass

  def create_temp_dirs_and_files(self, submission_id, test_case_id, input_content, expected_output_content, source_file_content):
    submission_dir = f'{tmp_dir}/{submission_id}'
    test_case_dir = f'{submission_dir}/{test_case_id}'
    
    self.create_temp_dir(submission_dir)
    self.create_temp_dir(test_case_dir)

    self.create_temp_file(test_case_dir, 'input.txt', input_content)
    self.create_temp_file(test_case_dir, 'expected_output.txt', expected_output_content)
    self.create_temp_file(test_case_dir, self.source_file_name, source_file_content)

  def run_process(self, command, timeout=1):
    try:
      return subprocess.run(command,
              stdout=subprocess.PIPE,
              stderr=subprocess.PIPE,
              check=True, shell=True, timeout=timeout)
    except subprocess.TimeoutExpired as error:
      log.error('Timeout Error:')
      raise TimeoutError(f'TimeoutError: {command}')

  def run_compiler(self):
    pass
  
  def run_executable(self):
    pass

  def compare_outputs(self):
    command = f'diff -E -b -w -B {self.work_dir}/expected_output.txt {self.work_dir}/computed_output.txt'
    log.info(f'Executing Diff: {command}')
    try:
      self.run_process(command)
    except subprocess.CalledProcessError as error:
      log.error(f'Diff Error: {error.stderr}')
      raise DiffError('DiffError')

  def run(self, submission_id, test_case_id, input_content, expected_output_content, source_file_content):
    log.info('-' * 80)
    log.info('Submission Runner Started')
    self.create_temp_dirs_and_files(submission_id, test_case_id, input_content, expected_output_content, source_file_content)
    # To-do Refactor: get files paths from creation method 
    self.work_dir = f'{tmp_dir}/{submission_id}/{test_case_id}'
    try:
      self.run_compiler()
      self.run_executable()
      self.compare_outputs()
    except SubmissionError as error:
      log.info(error.message) 
      return error.message
    log.info('OK')  
    return 'OK'


class C_SubmissionRunner(SubmissionRunner):
  def __init__(self):
    super().__init__()
    self.source_file_name = 'main.c'
  
  def run_compiler(self):
    command = f'gcc -o {self.work_dir}/main {self.work_dir}/{self.source_file_name} 2> {self.work_dir}/compiler.err.out'
    log.info(f'Executing C Compiler: {command}')
    try:
      self.run_process(command)
    except subprocess.CalledProcessError as error:
      log.error(f'Sintax Error: {error.stderr}')
      raise SintaxError('SintaxError')
  
  def run_executable(self):
    command = f'{self.work_dir}/main < {self.work_dir}/input.txt > {self.work_dir}/computed_output.txt'
    log.info(f'Executing Program: {command}')
    try:
      self.run_process(command)
    except subprocess.CalledProcessError as error:
      log.error(f'Runtime Error: {error.stderr}')
      raise RuntimeError('RuntimeError')


class JAVA_SubmissionRunner(SubmissionRunner):
  def __init__(self):
    super().__init__()
    self.source_file_name = 'Principal.java'
  
  def run_compiler(self):
    command = f'javac {self.work_dir}/{self.source_file_name} 2> {self.work_dir}/compiler.err.out'
    log.info(f'Executing JAVA Compiler: {command}')
    try:
      self.run_process(command, timeout=3)
    except subprocess.CalledProcessError as error:
      log.error(f'Sintax Error: {error.stderr}')
      raise SintaxError('SintaxError')
  
  def run_executable(self):
    command = f'java -cp {self.work_dir} Principal < {self.work_dir}/input.txt > {self.work_dir}/computed_output.txt'
    log.info(f'Executing Program: {command}')
    try:
      self.run_process(command)
    except subprocess.CalledProcessError as error:
      log.error(f'Runtime Error: {error.stderr}')
      raise RuntimeError('RuntimeError')

class Python_SubmissionRunner(SubmissionRunner):
  def __init__(self):
    super().__init__()
    self.source_file_name = 'main.py'
  
  def run_compiler(self):
    command = f'python -m py_compile {self.work_dir}/{self.source_file_name} 2> {self.work_dir}/compiler.err.out'
    log.info(f'Executing Python Compiler: {command}')
    try:
      self.run_process(command, timeout=3)
    except subprocess.CalledProcessError as error:
      log.error(f'Sintax Error: {error.stderr}')
      raise SintaxError('SintaxError')
  
  def run_executable(self):
    command = f'python {self.work_dir}/{self.source_file_name} < {self.work_dir}/input.txt > {self.work_dir}/computed_output.txt'
    log.info(f'Executing Program: {command}')
    try:
      self.run_process(command)
    except subprocess.CalledProcessError as error:
      log.error(f'Runtime Error: {error.stderr}')
      raise RuntimeError('RuntimeError')
      
  

if __name__ == "__main__":  
  submission_id = 0
  test_case_id = 0 
  input_content = '' 
  expected_output_content = 'Ola Mundo' 
  c_source_file_content = 'int main(void) {puts("Ola Mundo"); return 0;}'
  java_source_file_content = """class Principal { 
  public static void main(String[] args) {
    System.out.println("Ola Mundo");
  } 
}
"""
  python_source_file_content = 'print("Ola Mundo")'

  C_SubmissionRunner().run(0, 1, input_content, expected_output_content, c_source_file_content)
  JAVA_SubmissionRunner().run(1, 1, input_content, expected_output_content, java_source_file_content)
  Python_SubmissionRunner().run(2, 1, input_content, expected_output_content, python_source_file_content)
  
  input_content = 'Ola Mundo' 
  python_source_file_content = 'print(input())'
  Python_SubmissionRunner().run(3, 1, input_content, expected_output_content, python_source_file_content)