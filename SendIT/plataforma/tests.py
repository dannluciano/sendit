from django.test import TestCase
from .businnes import run_submission


class BussinessTestCase(TestCase):
    def test_run_ok_submission(self):
        code = """console.log('Hello World!')"""
        expected_input = ''
        expected_output = 'Hello World!\n'
        result = run_submission(code, expected_input, expected_output)
        self.assertEqual(result, 'OK')

    def test_run_ok_submission_with_blank_spaces(self):
        code = """console.log(' Hello World! ')"""
        expected_input = ''
        expected_output = 'Hello World!\n'
        result = run_submission(code, expected_input, expected_output)
        self.assertEqual(result, 'OK')

    def test_run_ok_submission_with_blank_lines(self):
        code = """console.log("\\nHello World!\\n")"""
        expected_input = ''
        expected_output = 'Hello World!'
        result = run_submission(code, expected_input, expected_output)
        self.assertEqual(result, 'OK')

    def test_run_ok_submission_with_alert(self):
        code = """alert('Hello World!')"""
        expected_input = ''
        expected_output = 'Hello World!\n'
        result = run_submission(code, expected_input, expected_output)
        self.assertEqual(result, 'OK')

    def test_run_ok_submission_with_prompt(self):
        code = """
for (let i = 0; i < 5; i++) {
    num = parseInt(prompt())
    alert(Math.pow(num, 2))
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
        result = run_submission(code, expected_input, expected_output)
        self.assertEqual(result, 'OK')

    def test_run_ok_submission_with_confirm_true(self):
        code = """
for (let i = 1; i <= 10; i++) {
    alert(confirm())
}
"""
        expected_input = """Yes
yes
Y
y
Sim
sim
S
s
Ok
ok
1
"""

        expected_output = """
true
true
true
true
true
true
true
true
true
true
"""
        result = run_submission(code, expected_input, expected_output)
        self.assertEqual(result, 'OK')

    def test_run_ok_submission_with_confirm_false(self):
        code = """
for (let i = 1; i <= 10; i++) {
    alert(confirm())
}
"""
        expected_input = """No
no
N
n
Nao
nao
N
n
0
Não
"""

        expected_output = """
false
false
false
false
false
false
false
false
false
false
"""
        result = run_submission(code, expected_input, expected_output)
        self.assertEqual(result, 'OK')

    def test_run_submission_with_prompt_loop(self):
        code = """prompt()"""
        expected_input = ''
        expected_output = 'Hello World'
        result = run_submission(code, expected_input, expected_output)
        self.assertEqual(result, 'JSRuntimeError')

    def test_run_submission_with_sintax_error(self):
        code = """
if 1 < 2 {
console.log('Hello World!')
}
"""
        expected_input = ''
        expected_output = ''
        result = run_submission(code, expected_input, expected_output)
        self.assertEqual(result, 'JSSintaxError')

    def test_run_submission_with_runtime_error(self):
        code = """
function fat(n) {
    if (n < 2) {
        return 1
    }
    return n * fat(n-1)
}
fat(65536)
"""
        expected_input = ''
        expected_output = ''
        result = run_submission(code, expected_input, expected_output)
        self.assertEqual(result, 'JSRuntimeError')

    def test_run_submission_with_timeout_error(self):
        code = """
while (true) {
}
"""
        expected_input = ''
        expected_output = ''
        result = run_submission(code, expected_input, expected_output)
        self.assertEqual(result, 'JSTimeoutError')

    def test_run_submission_with_diff_error(self):
        code = """
for (let i = 1; i <= 10; i++) {
    console.log('i')
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
        result = run_submission(code, expected_input, expected_output)
        self.assertEqual(result, 'DiffError')
