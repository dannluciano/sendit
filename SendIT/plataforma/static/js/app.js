/* eslint-env browser, jquery */
/* global ace */

function activateAcePlugin (editor, lang, newSubmission) {
  switch (lang) {
    case 'c':
      editor.getSession().setMode('ace/mode/c_cpp')
      if (newSubmission) {
        editor.getSession().setValue('#include <stdio.h>')
      }
      break
    case 'java':
      editor.getSession().setMode('ace/mode/java')
      if (newSubmission) {
        editor.getSession().setValue('class Principal {\n}')
      }
      break
    case 'python':
      editor.getSession().setMode('ace/mode/python')
      if (newSubmission) {
        editor.getSession().setValue('print("Ola Mundo")')
      }
      break
    default:
  }
}

jQuery(document)
    .ready(function () {
      var editor = ace.edit('editor')
      editor.setTheme('ace/theme/github')
      editor.getSession().setMode('ace/mode/c')
      editor.setFontSize(20)
      editor.$blockScrolling = Infinity

      var textarea = $('textarea[name="editor"]')
      textarea.val(editor.getSession().getValue())

      editor.getSession().on('change', function () {
        textarea.val(editor.getSession().getValue())
      })

      $('#botao-executar').click(function (evt) {
        $('#code').submit()
      })

      $('#language-select').on('change', function () {
        var lang = $('#language-select').val()
        activateAcePlugin(editor, lang, true)
      })
      if (textarea.val() !== '') {
        var lang = $('#language-select').val()
        activateAcePlugin(editor, lang, false)
      }

      $('#code').submit(function (evt) {
        var lang = $('#language-select').val()
        if (lang === '_') {
          evt.preventDefault()
        }
      })
    })
