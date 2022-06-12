import logging

from django.contrib.auth.models import User
from django.test import TestCase, tag

from .models import Question, Submission
from .submission_runner import (C_SubmissionRunner, JAVA_SubmissionRunner,
                                JavaScript_SubmissionRunner,
                                Python_SubmissionRunner)

logging.disable(logging.CRITICAL)


@tag("unit")
class C_SubmissionWithoutExpectedOutputTestCase(TestCase):
    def test_run_ok_submission(self):
        work_dir = "tests/c/0/1"
        input_content = """Joao"""
        expected_output_content = "Ola, Joao"
        source_file_content = """
            #include <stdio.h>
            int main(void) {
                char str[5];
                scanf("%s", str);
                printf("Ola, %s", str);
            }
        """
        result = C_SubmissionRunner(
            work_dir, input_content, None, source_file_content
        ).run()
        self.assertEqual(result["status"], "OK")
        self.assertEqual(result["output"], expected_output_content)


@tag("c")
class C_SubmissionRunnerTestCase(TestCase):
    def test_run_ok_submission(self):
        work_dir = "tests/c/0/1"
        input_content = """Joao"""
        expected_output_content = """Ola, Joao"""
        source_file_content = """
            #include <stdio.h>
            int main(void) {
                char str[5];
                scanf("%s", str);
                printf("Ola, %s", str);
            }
        """
        result = C_SubmissionRunner(
            work_dir, input_content, expected_output_content, source_file_content
        ).run()
        self.assertEqual(result["status"], "OK")

    def test_run_sintax_error_submission(self):
        work_dir = "tests/c/0/2"
        input_content = """Joao"""
        expected_output_content = """Ola, Joao"""
        source_file_content = """
            #include <stdio.h>
            int main(void) {
                char str[5]
                scanf("%s", str)
                printf("Ola, %s", str)
            
        """
        result = C_SubmissionRunner(
            work_dir, input_content, expected_output_content, source_file_content
        ).run()
        self.assertEqual(result["status"], "SintaxError")

    def test_run_runtime_error_submission(self):
        work_dir = "tests/c/0/3"
        input_content = """Joao"""
        expected_output_content = """Ola, Joao"""
        source_file_content = """
            #include <stdio.h>
            int main(void) {
                char* str = 0;
                char* nome = *str;
                printf("Ola, %s", nome);
            }
        """
        result = C_SubmissionRunner(
            work_dir, input_content, expected_output_content, source_file_content
        ).run()
        self.assertEqual(result["status"], "RuntimeError")

    def test_run_timeout_error_submission(self):
        work_dir = "tests/c/0/4"
        input_content = """Joao"""
        expected_output_content = """Ola, Joao"""
        source_file_content = """
            #include <stdio.h>
            int main(void) {
                char str[5];
                scanf("%s", str);
                while(1){
                    printf("Ola, %s", str);
                }
            }
        """
        result = C_SubmissionRunner(
            work_dir, input_content, expected_output_content, source_file_content
        ).run()
        self.assertEqual(result["status"], "TimeoutError")

    def test_run_diff_error_submission(self):
        work_dir = "tests/c/0/5"
        input_content = """Joao"""
        expected_output_content = """Ola, Joao"""
        source_file_content = """
            #include <stdio.h>
            int main(void) {
                char str[5];
                scanf("%s", str);
                printf("Ola, %s", "Maria");
            }
        """
        result = C_SubmissionRunner(
            work_dir, input_content, expected_output_content, source_file_content
        ).run()
        self.assertEqual(result["status"], "DiffError")


@tag("javascript")
class JavaScript_SubmissionRunnerTestCase(TestCase):
    def test_run_ok_submission(self):
        work_dir = "tests/js/0/1"
        input_content = """Joao"""
        expected_output_content = """Ola, Joao"""
        source_file_content = """
            name = prompt()
            alert('Ola, ' + name)
        """
        result = JavaScript_SubmissionRunner(
            work_dir, input_content, expected_output_content, source_file_content
        ).run()
        self.assertEqual(result["status"], "OK")

    def test_run_sintax_error_submission(self):
        work_dir = "tests/js/0/2"
        input_content = """Joao"""
        expected_output_content = """Ola, Joao"""
        source_file_content = """
            name = prompt()
            alert('Ola, '  name)
        """
        result = JavaScript_SubmissionRunner(
            work_dir, input_content, expected_output_content, source_file_content
        ).run()
        self.assertEqual(result["status"], "SintaxError")

    def test_run_runtime_error_submission(self):
        work_dir = "tests/js/0/3"
        input_content = """Joao"""
        expected_output_content = """Ola, Joao"""
        source_file_content = """
            var name = null
            alert(name.joao)
        """
        result = JavaScript_SubmissionRunner(
            work_dir, input_content, expected_output_content, source_file_content
        ).run()
        self.assertEqual(result["status"], "RuntimeError")

    def test_run_timeout_error_submission(self):
        work_dir = "tests/js/0/4"
        input_content = """Joao"""
        expected_output_content = """Ola, Joao"""
        source_file_content = """
            while(true) {
                alert("Ola, Joao")
            }
        """
        result = JavaScript_SubmissionRunner(
            work_dir, input_content, expected_output_content, source_file_content
        ).run()
        self.assertEqual(result["status"], "TimeoutError")

    def test_run_diff_error_submission(self):
        work_dir = "tests/js/0/5"
        input_content = """Joao"""
        expected_output_content = """Ola, Joao"""
        source_file_content = """
            alert("Ola, Maria")
        """
        result = JavaScript_SubmissionRunner(
            work_dir, input_content, expected_output_content, source_file_content
        ).run()
        self.assertEqual(result["status"], "DiffError")


@tag("java")
class JAVA_SubmissionRunnerTestCase(TestCase):
    def test_run_ok_submission(self):
        work_dir = "tests/java/0/1"
        input_content = """Joao"""
        expected_output_content = """Ola, Joao"""
        source_file_content = """
            import java.util.Scanner;
            class Principal {
                public static void main (String[] args) {
                    Scanner entrada = new Scanner(System.in);
                    String nome = entrada.next();
                    System.out.println("Ola, " + nome);
                }
            }
        """
        result = JAVA_SubmissionRunner(
            work_dir, input_content, expected_output_content, source_file_content
        ).run()
        self.assertEqual(result["status"], "OK")

    def test_run_sintax_error_submission(self):
        work_dir = "tests/java/0/2"
        input_content = """Joao"""
        expected_output_content = """Ola, Joao"""
        source_file_content = """
            import java.util.Scanner;
            class Principal {
                public static void main (String[] args) {
                    Scanner entrada = new Scanner(System.in)
                    String nome = entrada.next()
                    System.out.println("Ola, " + nome)
                
            
        """
        result = JAVA_SubmissionRunner(
            work_dir, input_content, expected_output_content, source_file_content
        ).run()
        self.assertEqual(result["status"], "SintaxError")

    def test_run_runtime_error_submission(self):
        work_dir = "tests/java/0/3"
        input_content = """Joao"""
        expected_output_content = """Ola, Joao"""
        source_file_content = """
            import java.util.Scanner;
            class Principal {
                public static void main (String[] args) {
                    Scanner entrada = null;
                    String nome = entrada.next();
                    System.out.println("Ola, " + nome);
                }
            }
        """
        result = JAVA_SubmissionRunner(
            work_dir, input_content, expected_output_content, source_file_content
        ).run()
        self.assertEqual(result["status"], "RuntimeError")

    def test_run_timeout_error_submission(self):
        work_dir = "tests/java/0/4"
        input_content = """Joao"""
        expected_output_content = """Ola, Joao"""
        source_file_content = """
            import java.util.Scanner;
            class Principal {
                public static void main (String[] args) {
                    Scanner entrada = new Scanner(System.in);
                    String nome = entrada.next();
                    while(true) {
                        System.out.println("Ola, " + nome);
                    }
                }
            }
        """
        result = JAVA_SubmissionRunner(
            work_dir, input_content, expected_output_content, source_file_content
        ).run()
        self.assertEqual(result["status"], "TimeoutError")

    def test_run_diff_error_submission(self):
        work_dir = "tests/java/0/5"
        input_content = """Joao"""
        expected_output_content = """Ola, Joao"""
        source_file_content = """
            import java.util.Scanner;
            class Principal {
                public static void main (String[] args) {
                    Scanner entrada = new Scanner(System.in);
                    String nome = entrada.next();
                    System.out.println("Ola, Maria");
                }
            }
        """
        result = JAVA_SubmissionRunner(
            work_dir, input_content, expected_output_content, source_file_content
        ).run()
        self.assertEqual(result["status"], "DiffError")


@tag("python")
class Python_SubmissionRunnerTestCase(TestCase):
    def test_run_ok_submission(self):
        work_dir = "tests/python/0/1"
        input_content = """Joao"""
        expected_output_content = """Ola, Joao"""
        source_file_content = """
str = input()
print("Ola,", str)
"""
        result = Python_SubmissionRunner(
            work_dir, input_content, expected_output_content, source_file_content
        ).run()
        self.assertEqual(result["status"], "OK")

    def test_run_sintax_error_submission(self):
        work_dir = "tests/c/0/2"
        input_content = """Joao"""
        expected_output_content = """Ola, Joao"""
        source_file_content = """
str = input()
if str {
    print("Ola,", str)
}
"""
        result = Python_SubmissionRunner(
            work_dir, input_content, expected_output_content, source_file_content
        ).run()
        self.assertEqual(result["status"], "SintaxError")

    def test_run_runtime_error_submission(self):
        work_dir = "tests/python/0/3"
        input_content = """Joao"""
        expected_output_content = """Ola, Joao"""
        source_file_content = """
str = input()
pri.nt("Ola,", str)
"""
        result = Python_SubmissionRunner(
            work_dir, input_content, expected_output_content, source_file_content
        ).run()
        self.assertEqual(result["status"], "RuntimeError")

    def test_run_timeout_error_submission(self):
        work_dir = "tests/python/0/4"
        input_content = """Joao"""
        expected_output_content = """Ola, Joao"""
        source_file_content = """
str = input()
while(True):
    print("Ola,", str)
"""
        result = Python_SubmissionRunner(
            work_dir, input_content, expected_output_content, source_file_content
        ).run()
        self.assertEqual(result["status"], "TimeoutError")

    def test_run_diff_error_submission(self):
        work_dir = "tests/c/0/5"
        input_content = """Joao"""
        expected_output_content = """Ola, Joao"""
        source_file_content = """
str = input()
print("Ola, Maria")
"""
        result = Python_SubmissionRunner(
            work_dir, input_content, expected_output_content, source_file_content
        ).run()
        self.assertEqual(result["status"], "DiffError")
