from django.test import TestCase
from django.contrib.auth.models import User
from .models import Question, Submission


class SubmissionTestCase(TestCase):
    fixtures = ["seed"]

    def test_submission_save_with_ok_and_case_test(self):
        question = Question.objects.first()
        user = User.objects.first()
        code = """
import java.util.*;
class Principal {
    public static void main(String args[]) {
        Scanner entrada = new Scanner(System.in);
        while(entrada.hasNextInt()) {
                int numero = entrada.nextInt();
                System.out.println(numero*numero);
        }
    }
}
"""
        language = "java"
        submission = Submission(
            question=question, author=user, code=code, language=language
        )
        submission.save()
        self.assertEqual(submission.status, "OK")

    def test_submission_save_with_error_in_first_case_test(self):
        question = Question.objects.first()
        user = User.objects.first()
        code = """
class Principal {
    public static void main(String args[]) {
        System.out.println("Ola!!!");
    }
}
"""
        language = "java"
        submission = Submission(
            question=question, author=user, code=code, language=language
        )
        submission.save()
        self.assertEqual(submission.status, "DiffError")


from .submission_runner import C_SubmissionRunner


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
        self.assertEqual(result, "OK")

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
        self.assertEqual(result, "SintaxError")

    def test_run_runtime_error_submission(self):
        work_dir = "tests/c/0/3"
        input_content = """Joao"""
        expected_output_content = """Ola, Joao"""
        source_file_content = """
            #include <stdio.h>
            int main(void) {
                char* str;
                char* nome = *str;
                printf("Ola, %s", nome);
            }
            
        """
        result = C_SubmissionRunner(
            work_dir, input_content, expected_output_content, source_file_content
        ).run()
        self.assertEqual(result, "RuntimeError")

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
        self.assertEqual(result, "TimeoutError")

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
        self.assertEqual(result, "DiffError")


from .submission_runner import JAVA_SubmissionRunner


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
        self.assertEqual(result, "OK")

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
        self.assertEqual(result, "SintaxError")

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
        self.assertEqual(result, "RuntimeError")

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
        self.assertEqual(result, "TimeoutError")

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
        self.assertEqual(result, "DiffError")


from .submission_runner import Python_SubmissionRunner


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
        self.assertEqual(result, "OK")

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
        self.assertEqual(result, "SintaxError")

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
        self.assertEqual(result, "RuntimeError")

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
        self.assertEqual(result, "TimeoutError")

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
        self.assertEqual(result, "DiffError")
