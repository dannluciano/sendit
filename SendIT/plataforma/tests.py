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


from .submission_runner import C_SubmissionRunner
class C_SubmissionRunnerTestCase(TestCase):
    def test_run_ok_submission(self):
        work_dir = 'tests/c/0/1'
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
        result = C_SubmissionRunner(work_dir, input_content, expected_output_content, source_file_content).run()
        self.assertEqual(result, 'OK')


    def test_run_sintax_error_submission(self):
        work_dir = 'tests/c/0/2'
        input_content = """Joao"""
        expected_output_content = """Ola, Joao"""
        source_file_content = """
            #include <stdio.h>
            int main(void) {
                char str[5]
                scanf("%s", str)
                printf("Ola, %s", str)
            
        """
        result = C_SubmissionRunner(work_dir, input_content, expected_output_content, source_file_content).run()
        self.assertEqual(result, 'SintaxError')
    
    def test_run_runtime_error_submission(self):
        work_dir = 'tests/c/0/3'
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
        result = C_SubmissionRunner(work_dir, input_content, expected_output_content, source_file_content).run()
        self.assertEqual(result, 'RuntimeError')

    def test_run_timeout_error_submission(self):
        work_dir = 'tests/c/0/4'
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
        result = C_SubmissionRunner(work_dir, input_content, expected_output_content, source_file_content).run()
        self.assertEqual(result, 'TimeoutError')

    def test_run_diff_error_submission(self):
        work_dir = 'tests/c/0/5'
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
        result = C_SubmissionRunner(work_dir, input_content, expected_output_content, source_file_content).run()
        self.assertEqual(result, 'DiffError')


from .submission_runner import JAVA_SubmissionRunner
class JAVA_SubmissionRunnerTestCase(TestCase):
    def test_run_ok_submission(self):
        work_dir = 'tests/java/0/1'
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
        result = JAVA_SubmissionRunner(work_dir, input_content, expected_output_content, source_file_content).run()
        self.assertEqual(result, 'OK')


    def test_run_sintax_error_submission(self):
        work_dir = 'tests/java/0/2'
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
        result = JAVA_SubmissionRunner(work_dir, input_content, expected_output_content, source_file_content).run()
        self.assertEqual(result, 'SintaxError')
    
    def test_run_runtime_error_submission(self):
        work_dir = 'tests/java/0/3'
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
        result = JAVA_SubmissionRunner(work_dir, input_content, expected_output_content, source_file_content).run()
        self.assertEqual(result, 'RuntimeError')

    def test_run_timeout_error_submission(self):
        work_dir = 'tests/java/0/4'
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
        result = JAVA_SubmissionRunner(work_dir, input_content, expected_output_content, source_file_content).run()
        self.assertEqual(result, 'TimeoutError')

    def test_run_diff_error_submission(self):
        work_dir = 'tests/java/0/5'
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
        result = JAVA_SubmissionRunner(work_dir, input_content, expected_output_content, source_file_content).run()
        self.assertEqual(result, 'DiffError')


from .submission_runner import Python_SubmissionRunner
class Python_SubmissionRunnerTestCase(TestCase):
    def test_run_ok_submission(self):
        work_dir = 'tests/python/0/1'
        input_content = """Joao"""
        expected_output_content = """Ola, Joao"""
        source_file_content = """
str = input()
print("Ola,", str)
"""
        result = Python_SubmissionRunner(work_dir, input_content, expected_output_content, source_file_content).run()
        self.assertEqual(result, 'OK')


    def test_run_sintax_error_submission(self):
        work_dir = 'tests/c/0/2'
        input_content = """Joao"""
        expected_output_content = """Ola, Joao"""
        source_file_content = """
str = input()
if str {
    print("Ola,", str)
}
"""
        result = Python_SubmissionRunner(work_dir, input_content, expected_output_content, source_file_content).run()
        self.assertEqual(result, 'SintaxError')
    
    def test_run_runtime_error_submission(self):
        work_dir = 'tests/python/0/3'
        input_content = """Joao"""
        expected_output_content = """Ola, Joao"""
        source_file_content = """
str = input()
pri.nt("Ola,", str)
"""
        result = Python_SubmissionRunner(work_dir, input_content, expected_output_content, source_file_content).run()
        self.assertEqual(result, 'RuntimeError')

    def test_run_timeout_error_submission(self):
        work_dir = 'tests/python/0/4'
        input_content = """Joao"""
        expected_output_content = """Ola, Joao"""
        source_file_content = """
str = input()
while(True):
    print("Ola,", str)
"""
        result = Python_SubmissionRunner(work_dir, input_content, expected_output_content, source_file_content).run()
        self.assertEqual(result, 'TimeoutError')

    def test_run_diff_error_submission(self):
        work_dir = 'tests/c/0/5'
        input_content = """Joao"""
        expected_output_content = """Ola, Joao"""
        source_file_content = """
str = input()
print("Ola, Maria")
"""
        result = Python_SubmissionRunner(work_dir, input_content, expected_output_content, source_file_content).run()
        self.assertEqual(result, 'DiffError')