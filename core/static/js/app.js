/* eslint-env browser, jquery */
/* global ace */

ace.config.set('basePath', '/static/js/')

function activateAcePlugin (editor, lang, newSubmission) {
  switch (lang) {
    case 'c':
      editor.getSession().setMode('ace/mode/c_cpp')
      if (newSubmission) {
        editor.getSession().setValue('#include <stdio.h>')
      }
      break
    case 'c++11':
      editor.getSession().setMode('ace/mode/c_cpp')
      if (newSubmission) {
        editor.getSession().setValue('#include <iostream>')
      }
      break
    case 'javascript':
      editor.getSession().setMode('ace/mode/javascript')
      if (newSubmission) {
        editor.getSession().setValue('alert("Ola Mundo")')
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

function setEditorTheme () {
  var theme = document.body.dataset.theme || 'ligth'
  var editor = ace.edit('editor')
  editor.setTheme('ace/theme/tomorrow_' + theme)
}

jQuery(document)
  .ready(function () {
    setEditorTheme()
    var editor = ace.edit('editor')
    editor.setFontSize(24)
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
