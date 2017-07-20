/* eslint-env browser, jquery */
/* global ace */

jQuery(document)
  .ready(() => {
    var editor = ace.edit('editor')
    editor.setTheme('ace/theme/github')
    editor.getSession()
      .setMode('ace/mode/javascript')
    editor.setFontSize(20)

    var textarea = $('textarea[name="editor"]')
    textarea.val(editor.getSession()
      .getValue())

    editor.getSession()
      .on('change', () => {
        textarea.val(editor.getSession()
          .getValue())
      })

    $('#botao-executar')
      .click((evt) => {
        $('#code')
          .submit()
      })
  })
