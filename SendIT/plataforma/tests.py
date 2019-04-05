from django.test import TestCase
from django.contrib.auth.models import User
from .models import Question, Submission
from .businnes import run_submission


class SubmissionTestCase(TestCase):
    fixtures = ['seed']

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
        submission = Submission(questao=question, autor=user, codigo=code)
        submission.save()
        self.assertEqual(submission.status, 'OK')

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
        submission = Submission(questao=question, autor=user, codigo=code)
        submission.save()
        self.assertEqual(submission.status, 'DiffError')


class BussinessTestCase(TestCase):
    def test_run_ok_submission(self):
        code = """
class Principal {
    public static void main(String args[]) {
        System.out.println("Hello World!");
    }
}
"""
        expected_input = ''
        expected_output = 'Hello World!\n'
        result = run_submission('test_run_ok_submission', code, expected_input, expected_output)
        self.assertEqual(result, 'OK')

    def test_run_ok_submission_with_blank_spaces(self):
        code = """
class Principal {
    public static void main(String args[]) {
        System.out.println("   Hello World!   ");
    }
}
"""
        expected_input = ''
        expected_output = 'Hello World!\n'
        result = run_submission('test_run_ok_submission_with_blank_spaces', code, expected_input, expected_output)
        self.assertEqual(result, 'OK')

    def test_run_ok_submission_with_blank_lines(self):
        code = """
class Principal {
    public static void main(String args[]) {
        System.out.println("\\nHello World!\\n");
    }
}
"""
        expected_input = ''
        expected_output = 'Hello World!'
        result = run_submission('test_run_ok_submission_with_blank_lines', code, expected_input, expected_output)
        self.assertEqual(result, 'OK')


    def test_run_ok_submission_with_prompt(self):
        code = """
import java.util.Scanner;
class Principal {
    public static void main(String args[]) {
            Scanner entrada = new Scanner(System.in);
            for (int i = 0; i < 5; i++) {
                    int numero = entrada.nextInt();
                    System.out.println(numero*numero);
            }
        
    }
}
"""
        expected_input = """2
4
6
8
10
"""

        expected_output = """4
16
36
64
100
"""
        result = run_submission('test_run_ok_submission_with_prompt', code, expected_input, expected_output)
        self.assertEqual(result, 'OK')


    def test_run_submission_with_sintax_error(self):
        code = """
if 1 < 2 {
        System.out.println("Ola")
}
"""
        expected_input = ''
        expected_output = ''
        result = run_submission('test_run_submission_with_sintax_error', code, expected_input, expected_output)
        self.assertEqual(result, 'SintaxError')

    def test_run_submission_with_runtime_error(self):
        code = """
import java.util.Scanner;
class Principal {
    public static void main(String args[]) {
            for (int i = 0; i < 5; i++) {
                    Scanner entrada = null;
                    int numero = entrada.nextInt();
                    System.out.println(numero*numero);
            }
        
    }
}
"""
        expected_input = ''
        expected_output = ''
        result = run_submission('test_run_submission_with_runtime_error', code, expected_input, expected_output)
        self.assertEqual(result, 'RuntimeError')

    def test_run_submission_with_timeout_error(self):
        code = """
class Principal {
    public static void main(String args[]) {
            for (; ; ) {
                    System.out.println("oi");
            }
        
    }
}
"""
        expected_input = ''
        expected_output = ''
        result = run_submission('test_run_submission_with_timeout_error', code, expected_input, expected_output)
        self.assertEqual(result, 'TimeoutError')

    def test_run_submission_with_diff_error(self):
        code = """
class Principal {
    public static void main(String args[]) {
            for (int i = 0; i < 5; i++) {
                    System.out.println(i);
            }
        
    }
}
"""
        expected_input = ''
        expected_output = """
1
2
3
4
5
6
7
8
9
10
"""
        result = run_submission('test_run_submission_with_diff_error', code, expected_input, expected_output)
        self.assertEqual(result, 'DiffError')
