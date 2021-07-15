/* global CodeMirror */

document.addEventListener('DOMContentLoaded', function () {
  const csrftoken = document.querySelector('[name=csrfmiddlewaretoken]').value

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
    java: 'class Principal {\n\tpublic static void main(String[] args) {\n\t\tSystem.out.println("Ola Mundo");\n\t}\n}',
    javascript: 'console.log("Ola Mundo")',
    python: 'print("Ola Mundo")'
  }

  const editorTextArea = document.getElementById('editor')
  const editor = CodeMirror.fromTextArea(editorTextArea, {
    lineNumbers: true,
    readOnly: true,
    theme: 'solarized',
    viewportMargin: Infinity
  })

  const inputField = document.getElementById('input')

  function setupLanguage (language) {
    if (language !== 'null') {
      editor.setOption('mode', languagesMode[language])
      editor.setOption('readOnly', false)
      editor.setValue(languagesHelloWorld[language])
      console.log('Changed Language to:' + language + ':' + editor.getOption('mode'))
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

  const runButton = document.getElementById('run-button')
  if (runButton) {
    runButton.addEventListener('click', function (event) {
      console.log('Sending code to Runner...')

      const code = editor.getValue()
      const lang = languageSelector.value
      const input = inputField.value

      if (lang === 'null') { return }

      startLoading()

      const options = {
        method: 'POST',
        credentials: 'same-origin',
        headers: {
          'X-CSRFToken': csrftoken
        },
        body: JSON.stringify({
          code: code,
          lang: lang,
          input: input
        })
      }
      fetch('/editor/runner/', options)
        .then(function (response) {
          response.json().then(function (json) {
            setupInterval(json.uuid)
          })
        })
    })
  }
})

let runnerInterval = null

function setupInterval (runnerUUID) {
  runnerInterval = setInterval(() => {
    console.log('Getting Runner status: ', runnerUUID)
    const runnerStatusURL = '/editor/runner/' + runnerUUID + '/'
    fetch(runnerStatusURL)
      .then(function (response) {
        response.json().then(function (runner) {
          console.info(runner)
          updateUI(runner)
          if (runner.status !== 'Waiting') {
            clearInterval(runnerInterval)
            stopLoading()
          }
        })
      })
  }, 1000)
}

function updateUI (runner) {
  const output = document.getElementById('output')
  output.innerText = runner.output
}

const loader = document.querySelector('.loader-wrapper')

function startLoading () {
  console.info('Start Loading')
  loader.classList.add('is-active')
}

function stopLoading () {
  console.info('Stoping Loading')
  loader.classList.remove('is-active')
}
