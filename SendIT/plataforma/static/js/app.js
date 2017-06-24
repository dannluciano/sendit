/* eslint-env browser, jquery */
/* global ace */

jQuery(document)
  .ready(() => {
    var editor = ace.edit('editor')
    editor.setTheme('ace/theme/github')
    editor.getSession()
      .setMode('ace/mode/javascript')
    editor.setFontSize(20)
  })
