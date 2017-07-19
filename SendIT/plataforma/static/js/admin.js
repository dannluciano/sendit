/* eslint-env browser, jquery */
/* global django, ace */

(function ($) {
    function setupAce(field) {
        var editor = ace.edit(`id_${field}`);
        editor.setTheme('ace/theme/github');
        editor.getSession()
            .setMode('ace/mode/javascript');
        editor.setFontSize(16);

        var textarea = $('<textarea></textarea>', {
            id: `id_${field}`,
            style: 'visibility: hidden; display: none',
            name: '${field}'
        }).appendTo(`.field-${field}`);

        editor.getSession()
            .on('change', function () {
                textarea.val(editor.getSession()
                    .getValue())
            });

        editor.insert('\n')
    }

    $(function () {
        setupAce('pre_codigo');
        setupAce('pos_codigo');

        $('pre.ace_editor').css('height', '800px')
    })
})(django.jQuery)
