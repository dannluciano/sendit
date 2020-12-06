/* global CodeMirror */

document.addEventListener('DOMContentLoaded', function () {
  const languagesMode = {
    c: 'text/x-csrc',
    cplusplus: 'text/x-c++src',
    java: 'text/x-java',
    javascript: 'javascript',
    python: 'python'
  }

  const languagesHelloWorld = {
    c: '#include <stdio.h>\nint main() {\n\tputs("Ola Mundo");\n\treturn 0;\n}\n',
    cplusplus: '#include <iostream>\nint main() {\n\tstd::cout << "Ola Mundo" << std::endl;\n\treturn 0;\n}',
    java: 'class Main {\n\tpublic static void main(String[] args) {\n\t\tSystem.out.println("Ola Mundo");\n\t}\n}',
    javascript: 'console.log("Ola Mundo")',
    python: 'print("Ola Mundo")'
  }

  const editor = CodeMirror.fromTextArea(document.getElementById('editor'), {
    lineNumbers: true,
    readOnly: true,
    theme: 'solarized',
    viewportMargin: Infinity
  })

  const languageSelector = document.getElementById('language-select')
  if (languageSelector) {
    languageSelector.addEventListener('change', function (event) {
      const language = event.target.value
      if (language !== 'null') {
        editor.setOption('mode', languagesMode[language])
        editor.setOption('readOnly', false)
        editor.setValue(languagesHelloWorld[language])
        console.log('Changed Language to:' + language + ':' + editor.getOption('mode'))
      }
    })
  }
})
