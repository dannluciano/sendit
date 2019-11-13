ace.define('ace/theme/tomorrow_ligth', ['require', 'exports', 'module', 'ace/lib/dom'], function (require, exports, module) {
    exports.isDark = false
    exports.cssClass = 'ace-tomorrow-ligth'
    exports.cssText = '.ace-tomorrow-ligth .ace_gutter {\
background: #f6f6f6;\
color: #4D4D4C\
}\
.ace-tomorrow-ligth .ace_print-margin {\
width: 1px;\
background: #f6f6f6\
}\
.ace-tomorrow-ligth {\
background-color: #FFFFFF;\
color: #4D4D4C\
}\
.ace-tomorrow-ligth .ace_cursor {\
color: #AEAFAD\
}\
.ace-tomorrow-ligth .ace_marker-layer .ace_selection {\
background: #D6D6D6\
}\
.ace-tomorrow-ligth.ace_multiselect .ace_selection.ace_start {\
box-shadow: 0 0 3px 0px #FFFFFF;\
}\
.ace-tomorrow-ligth .ace_marker-layer .ace_step {\
background: rgb(255, 255, 0)\
}\
.ace-tomorrow-ligth .ace_marker-layer .ace_bracket {\
margin: -1px 0 0 -1px;\
border: 1px solid #D1D1D1\
}\
.ace-tomorrow-ligth .ace_marker-layer .ace_active-line {\
background: #EFEFEF\
}\
.ace-tomorrow-ligth .ace_gutter-active-line {\
background-color : #dcdcdc\
}\
.ace-tomorrow-ligth .ace_marker-layer .ace_selected-word {\
border: 1px solid #D6D6D6\
}\
.ace-tomorrow-ligth .ace_invisible {\
color: #D1D1D1\
}\
.ace-tomorrow-ligth .ace_keyword,\
.ace-tomorrow-ligth .ace_meta,\
.ace-tomorrow-ligth .ace_storage,\
.ace-tomorrow-ligth .ace_storage.ace_type,\
.ace-tomorrow-ligth .ace_support.ace_type {\
color: #8959A8\
}\
.ace-tomorrow-ligth .ace_keyword.ace_operator {\
color: #3E999F\
}\
.ace-tomorrow-ligth .ace_constant.ace_character,\
.ace-tomorrow-ligth .ace_constant.ace_language,\
.ace-tomorrow-ligth .ace_constant.ace_numeric,\
.ace-tomorrow-ligth .ace_keyword.ace_other.ace_unit,\
.ace-tomorrow-ligth .ace_support.ace_constant,\
.ace-tomorrow-ligth .ace_variable.ace_parameter {\
color: #F5871F\
}\
.ace-tomorrow-ligth .ace_constant.ace_other {\
color: #666969\
}\
.ace-tomorrow-ligth .ace_invalid {\
color: #FFFFFF;\
background-color: #C82829\
}\
.ace-tomorrow-ligth .ace_invalid.ace_deprecated {\
color: #FFFFFF;\
background-color: #8959A8\
}\
.ace-tomorrow-ligth .ace_fold {\
background-color: #4271AE;\
border-color: #4D4D4C\
}\
.ace-tomorrow-ligth .ace_entity.ace_name.ace_function,\
.ace-tomorrow-ligth .ace_support.ace_function,\
.ace-tomorrow-ligth .ace_variable {\
color: #4271AE\
}\
.ace-tomorrow-ligth .ace_support.ace_class,\
.ace-tomorrow-ligth .ace_support.ace_type {\
color: #C99E00\
}\
.ace-tomorrow-ligth .ace_heading,\
.ace-tomorrow-ligth .ace_markup.ace_heading,\
.ace-tomorrow-ligth .ace_string {\
color: #718C00\
}\
.ace-tomorrow-ligth .ace_entity.ace_name.ace_tag,\
.ace-tomorrow-ligth .ace_entity.ace_other.ace_attribute-name,\
.ace-tomorrow-ligth .ace_meta.ace_tag,\
.ace-tomorrow-ligth .ace_string.ace_regexp,\
.ace-tomorrow-ligth .ace_variable {\
color: #C82829\
}\
.ace-tomorrow-ligth .ace_comment {\
color: #8E908C\
}\
.ace-tomorrow-ligth .ace_indent-guide {\
background: url(data:image/png;base64,iVBORw0KGgoAAAANSUhEUgAAAAEAAAACCAYAAACZgbYnAAAAE0lEQVQImWP4////f4bdu3f/BwAlfgctduB85QAAAABJRU5ErkJggg==) right repeat-y\
}'

    var dom = require('../lib/dom')
    dom.importCssString(exports.cssText, exports.cssClass)
})
