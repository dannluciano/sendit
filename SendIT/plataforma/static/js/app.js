/* eslint-env browser, jquery */
/* global ace */

jQuery(document)
    .ready(function () {
        var editor = ace.edit('editor');
        editor.setTheme('ace/theme/github');
        editor.getSession().setMode('ace/mode/javascript');
        editor.setFontSize(20);

        var textarea = $('textarea[name="editor"]');
        textarea.val(editor.getSession().getValue());

        editor.getSession().on('change', function () {
            textarea.val(editor.getSession().getValue())
        });

        $('#botao-executar').click(function (evt) {
            $('#code').submit()
        });
    });
