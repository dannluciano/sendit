/* global CodeMirror, setupRunner */

document.addEventListener('DOMContentLoaded', function () {
  const languagesMode = {
    c: 'text/x-csrc',
    cplusplus: 'text/x-c++src',
    java: 'text/x-java',
    javascript: 'javascript',
    python: 'python'
  }

  const languagesHelloWorld = {
    c: '#include <stdio.h>\nint main() {\n    puts("Ola Mundo");\n    return 0;\n}\n',
    cplusplus: '#include <iostream>\nint main() {\n    std::cout << "Ola Mundo" << std::endl;\n    return 0;\n}',
    java: 'class Principal {\n    public static void main(String[] args) {\n        System.out.println("Ola Mundo");\n    }\n}',
    javascript: 'console.log("Ola Mundo")',
    python: 'print("Ola Mundo")'
  }

  const languagesConfig = {
    c: {
      indentUnit: 4
    },
    cplusplus: {
      indentUnit: 4
    },
    java: {
      indentUnit: 4
    },
    javascript: {
      indentUnit: 2
    },
    python: {
      indentUnit: 2
    }
  }

  const editorTextArea = document.getElementById('editor')
  if (!editorTextArea) { return }

  const editor = CodeMirror.fromTextArea(editorTextArea, {
    lineNumbers: true,
    readOnly: true,
    theme: 'solarized',
    viewportMargin: Infinity
  })

  function setupLanguage (language) {
    if (language !== 'null') {
      editor.setOption('mode', languagesMode[language])
      editor.setOption('readOnly', false)
      editor.setOption('indentUnit', languagesConfig[language].indentUnit)
      if (editor.getValue().length === 0) {
        editor.setValue(languagesHelloWorld[language])
      }
      console.log('Changed Language to:' + language + ':' + editor.getOption('mode') +
        ' Identation: ' + editor.getOption('indentUnit'))
    }
  }

  const languageSelector = document.getElementById('language-select')
  if (languageSelector) {
    const language = languageSelector.value
    setupLanguage(language)

    languageSelector.addEventListener('change', function (event) {
      const language = event.target.value
      setupLanguage(language)
    })
  }

  if (setupRunner) {
    setupRunner(editor, languageSelector)
  }
})
