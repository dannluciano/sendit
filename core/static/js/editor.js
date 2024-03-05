/* eslint-env browser */
/* global CodeMirror, Clipboard, setupRunner */

let pythonInstance = null;

document.addEventListener("DOMContentLoaded", function () {
  const languagesMode = {
    c: "text/x-csrc",
    cplusplus: "text/x-c++src",
    java: "text/x-java",
    javascript: "javascript",
    python: "python",
    pythonwasm: "python",
  };

  const languagesHelloWorld = {
    c: '#include <stdio.h>\nint main() {\n    puts("Ola Mundo");\n    return 0;\n}\n',
    cplusplus: '#include <iostream>\nint main() {\n    std::cout << "Ola Mundo" << std::endl;\n    return 0;\n}',
    java: 'class Principal {\n    public static void main(String[] args) {\n        System.out.println("Ola Mundo");\n    }\n}',
    javascript: 'console.log("Ola Mundo")',
    python: 'print("Ola Mundo")',
    pythonwasm: 'nome = input()\nprint("Ola", nome)',
  };

  const languagesConfig = {
    c: {
      indentUnit: 4,
    },
    cplusplus: {
      indentUnit: 4,
    },
    java: {
      indentUnit: 4,
    },
    javascript: {
      indentUnit: 2,
    },
    python: {
      indentUnit: 2,
    },
    pythonwasm: {
      indentUnit: 2,
    },
  };

  const editorTextArea = document.getElementById("editor");
  if (!editorTextArea) {
    return;
  }

  const editor = CodeMirror.fromTextArea(editorTextArea, {
    lineNumbers: true,
    readOnly: true,
    theme: "dracula",
    viewportMargin: Infinity,
    matchBrackets: true,
    gutters: ["CodeMirror-linenumbers"],
  });

  const variablesSection = document.getElementById("variables-section");
  const variables = document.getElementById("variables");
  const inputField = document.getElementById("input");
  const outputField = document.getElementById("output");

  function setupLanguage(language, force = false) {
    if (language !== "null") {
      if (outputField) {
        outputField.value = "";
      }
      editor.setOption("mode", languagesMode[language]);
      editor.setOption("readOnly", false);
      editor.setOption("indentUnit", languagesConfig[language].indentUnit);
      if (editor.getValue().length === 0 || force) {
        editor.setValue(languagesHelloWorld[language]);
      }
      console.log(
        "Changed Language to:" +
        language +
        ":" +
        editor.getOption("mode") +
        " Identation: " +
        editor.getOption("indentUnit")
      );
    }
    if (language === "pythonwasm") {
      setupPyodide().then(function (pyodide) {
        pythonInstance = pyodide;
        inputField.disabled = true;
        variables.disabled = false;
        variablesSection.classList.remove("is-hidden");
      });
    } else {
      if (inputField) {
        inputField.disabled = false;
      }
      if (variables && variablesSection) {
        variables.disabled = true;
        variablesSection.classList.add("is-hidden");
      }
    }
  }

  const languageSelector = document.getElementById("language-select");
  if (languageSelector) {
    const language = languageSelector.value;
    setupLanguage(language);

    languageSelector.addEventListener("change", function (event) {
      const language = event.target.value;
      setupLanguage(language, true);
    });
  }

  if (inputField && setupRunner) {
    setupRunner(editor, languageSelector);
  }

  const copyButton = document.getElementById("copy-button");
  if (copyButton) {
    const clipboard = new Clipboard(copyButton, {
      text: function (trigger) {
        return editor.getValue();
      },
    });

    clipboard.on("error", function (e) {
      console.error("Action:", e.action);
      console.error("Trigger:", e.trigger);
    });
  }

  const undoButton = document.getElementById("undo-button");
  if (undoButton) {
    undoButton.addEventListener("click", function (event) {
      editor.undo();
    });
  }

  const saveButton = document.getElementById("save-button");
  const filenameField = document.getElementById("filename");
  if (saveButton && filenameField) {
    saveButton.addEventListener("click", function (event) {
      saveButton.classList.add("is-loading");
      saveButton.classList.add("is-disabled");
      const filename = filenameField.value;
      const filesrc = editor.getValue();
      const language = languageSelector.value;

      if (filename.length === 0) {
        alert("Nome do Arquivo não pode ser vazio!");
        return;
      }

      if (filesrc.length === 0) {
        alert("Conteúdo do Arquivo não pode ser vazio!");
        return;
      }

      console.info("Saving ", filename, language);
      console.info(filesrc);

      const formData = new FormData();
      formData.append("filename", filename);
      formData.append("language", language);
      formData.append("filesrc", filesrc);

      const csrftoken = document.querySelector(
        "[name=csrfmiddlewaretoken]"
      ).value;
      const options = {
        method: "POST",
        credentials: "same-origin",
        headers: {
          "X-CSRFToken": csrftoken,
        },
        body: formData,
      };
      fetch("/editor/save/", options).then(function (response) {
        response.json().then(function (json) {
          console.info(json);
          saveButton.classList.remove("is-loading");
          saveButton.classList.remove("is-disabled");
        });
      });
    });
  }

  const formCode = document.getElementById("code");
  if (!formCode) {
    return;
  }

  formCode.addEventListener("submit", function (event) {
    if (
      languageSelector.value === "null" ||
      languageSelector.value === "pythonwasm"
    ) {
      event.preventDefault();
    }
  });
});