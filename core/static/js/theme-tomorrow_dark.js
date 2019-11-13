ace.define('ace/theme/tomorrow_dark', ['require', 'exports', 'module', 'ace/lib/dom'], function (require, exports, module) {
  exports.isDark = true
  exports.cssClass = 'ace-tomorrow-dark'
  exports.cssText = '.ace-tomorrow-dark .ace_gutter {\
    background: #25282c;\
    color: #C5C8C6\
    }\
    .ace-tomorrow-dark .ace_print-margin {\
    width: 1px;\
    background: #25282c\
    }\
    .ace-tomorrow-dark {\
    background-color: #1D1F21;\
    color: #C5C8C6\
    }\
    .ace-tomorrow-dark .ace_cursor {\
    color: #AEAFAD\
    }\
    .ace-tomorrow-dark .ace_marker-layer .ace_selection {\
    background: #373B41\
    }\
    .ace-tomorrow-dark.ace_multiselect .ace_selection.ace_start {\
    box-shadow: 0 0 3px 0px #1D1F21;\
    }\
    .ace-tomorrow-dark .ace_marker-layer .ace_step {\
    background: rgb(102, 82, 0)\
    }\
    .ace-tomorrow-dark .ace_marker-layer .ace_bracket {\
    margin: -1px 0 0 -1px;\
    border: 1px solid #4B4E55\
    }\
    .ace-tomorrow-dark .ace_marker-layer .ace_active-line {\
    background: #282A2E\
    }\
    .ace-tomorrow-dark .ace_gutter-active-line {\
    background-color: #282A2E\
    }\
    .ace-tomorrow-dark .ace_marker-layer .ace_selected-word {\
    border: 1px solid #373B41\
    }\
    .ace-tomorrow-dark .ace_invisible {\
    color: #4B4E55\
    }\
    .ace-tomorrow-dark .ace_keyword,\
    .ace-tomorrow-dark .ace_meta,\
    .ace-tomorrow-dark .ace_storage,\
    .ace-tomorrow-dark .ace_storage.ace_type,\
    .ace-tomorrow-dark .ace_support.ace_type {\
    color: #B294BB\
    }\
    .ace-tomorrow-dark .ace_keyword.ace_operator {\
    color: #8ABEB7\
    }\
    .ace-tomorrow-dark .ace_constant.ace_character,\
    .ace-tomorrow-dark .ace_constant.ace_language,\
    .ace-tomorrow-dark .ace_constant.ace_numeric,\
    .ace-tomorrow-dark .ace_keyword.ace_other.ace_unit,\
    .ace-tomorrow-dark .ace_support.ace_constant,\
    .ace-tomorrow-dark .ace_variable.ace_parameter {\
    color: #DE935F\
    }\
    .ace-tomorrow-dark .ace_constant.ace_other {\
    color: #CED1CF\
    }\
    .ace-tomorrow-dark .ace_invalid {\
    color: #CED2CF;\
    background-color: #DF5F5F\
    }\
    .ace-tomorrow-dark .ace_invalid.ace_deprecated {\
    color: #CED2CF;\
    background-color: #B798BF\
    }\
    .ace-tomorrow-dark .ace_fold {\
    background-color: #81A2BE;\
    border-color: #C5C8C6\
    }\
    .ace-tomorrow-dark .ace_entity.ace_name.ace_function,\
    .ace-tomorrow-dark .ace_support.ace_function,\
    .ace-tomorrow-dark .ace_variable {\
    color: #81A2BE\
    }\
    .ace-tomorrow-dark .ace_support.ace_class,\
    .ace-tomorrow-dark .ace_support.ace_type {\
    color: #F0C674\
    }\
    .ace-tomorrow-dark .ace_heading,\
    .ace-tomorrow-dark .ace_markup.ace_heading,\
    .ace-tomorrow-dark .ace_string {\
    color: #B5BD68\
    }\
    .ace-tomorrow-dark .ace_entity.ace_name.ace_tag,\
    .ace-tomorrow-dark .ace_entity.ace_other.ace_attribute-name,\
    .ace-tomorrow-dark .ace_meta.ace_tag,\
    .ace-tomorrow-dark .ace_string.ace_regexp,\
    .ace-tomorrow-dark .ace_variable {\
    color: #CC6666\
    }\
    .ace-tomorrow-dark .ace_comment {\
    color: #969896\
    }\
    .ace-tomorrow-dark .ace_indent-guide {\
    background: url(data:image/png;base64,iVBORw0KGgoAAAANSUhEUgAAAAEAAAACCAYAAACZgbYnAAAAEklEQVQImWNgYGBgYHB3d/8PAAOIAdULw8qMAAAAAElFTkSuQmCC) right repeat-y\
    }'

  var dom = require('../lib/dom')
  dom.importCssString(exports.cssText, exports.cssClass)
})
