/* eslint-env browser, jquery */
/* global ace */

var templates = {
  js: `console.log('Ola Mundo')`,
  java: `public class Programa {
    public static void main (String args[]) {
        System.out.println("Ola Mundo");
    }
  }`
}

jQuery(document)
  .ready(() => {
    var editor = ace.edit('editor')
    editor.setTheme('ace/theme/github')
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

    $('select[name="linguagem"]').on('change', (evt) => {
      var select = evt.target
      if (select.value === 'js') {
        editor.getSession()
          .setMode('ace/mode/javascript')
        editor.getSession()
          .setValue(templates['js'])
      }
      if (select.value === 'java') {
        editor.getSession()
          .setMode('ace/mode/java')
        editor.getSession()
          .setValue(templates['java'])
      }
    })
    console.log('ready')
  })
