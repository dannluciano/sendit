/* global fetch */

async function setupPyodide() {
  clearInput();
  clearOutptut();
  if (pythonInstance) {
    return pythonInstance;
  }
  startLoading();
  let pyodide = await loadPyodide({
    indexURL: "https://cdn.jsdelivr.net/pyodide/v0.20.0/full/",
    stdin: () => {
      let input = prompt();
      appendToInput(input + "\n");
      return input;
    },
    stdout: (str) => {
      appendToOutput(str + "\n");
      return str;
    },
    stderr: (str) => {
      appendToOutput(str + "\n");
      return str;
    },
  });
  stopLoading();
  return pyodide;
}

async function evaluatePython(source) {
  let pyodide = pythonInstance;
  try {
    const output = await pyodide.runPythonAsync(source);
    if (output) {
      return {
        status: "OK",
        output: output
      };
    }
    return {
      status: "OK",
      output: ""
    };
  } catch (err) {
    console.error(err);
    appendToOutput(err + "\n");
    return {
      status: "RuntimeError",
      output: err
    };
  }
}

function appendToOutput(str) {
  const output = document.getElementById("output");
  output.value += str;
}

function appendToInput(str) {
  const input = document.getElementById("input");
  input.value += str;
}

function addToVariables(map) {
  const variables = document.getElementById("variables");
  variables.value = "";
  for (const [key, value] of map) {
    if (
      !(key.startsWith("_") || key === "version_info" || key == "pyversion")
    ) {
      variables.value += key + ": " + value + "\n";
    }
  }
}

function clearOutptut() {
  const output = document.getElementById("output");
  if (output) {
    output.value = "";
  }
}

function clearInput() {
  const input = document.getElementById("input");
  if (input) {
    input.value = "";
  }
}

function clearVariables() {
  const variables = document.getElementById("variables");
  if (variables) {
    variables.value = "";
  }
}

async function evaluatePythonVars(source) {
  const pyodide = pythonInstance;
  const varsFinal = await pyodide.runPythonAsync("locals()");
  return varsFinal.toJs();
}

function makeMarker() {
  var marker = document.createElement("div");
  marker.style.color = "hsl(171, 100%, 41%)";
  marker.innerHTML = "&bull;";
  return marker;
}

function runPythonWASM(code) {
  clearInput();
  clearOutptut();
  clearVariables();
  evaluatePython(code).then(function (_runner) {
    evaluatePythonVars().then(function (map) {
      addToVariables(map);
    });
  });
}

function setupRunner(editor, languageSelector) {
  if (!languageSelector || !editor) {
    console.error("Can not Setup Runner without editor or languageSelector");
    return;
  }
  const inputField = document.getElementById("input");

  const runButton = document.getElementById("run-button");
  if (runButton) {
    runButton.addEventListener("click", function (event) {
      event.preventDefault();
      console.log("Sending code to Runner...");

      const code = editor.getValue();
      const lang = languageSelector.value;
      const input = inputField.value;

      if (lang === "null") {
        return;
      }

      if (lang === "pythonwasm") {
        runPythonWASM(code);
        return;
      }

      startLoading();

      const csrftoken = document.querySelector(
        "[name=csrfmiddlewaretoken]"
      ).value;

      const options = {
        method: "POST",
        credentials: "same-origin",
        headers: {
          "X-CSRFToken": csrftoken,
        },
        body: JSON.stringify({
          code: code,
          lang: lang,
          input: input,
        }),
      };
      fetch("/editor/runner/", options).then(function (response) {
        response.json().then(function (json) {
          setupInterval(json.uuid);
        });
      });
    });
  }
}

let runnerInterval = null;

function setupInterval(runnerUUID) {
  runnerInterval = setInterval(() => {
    console.log("Getting Runner status: ", runnerUUID);
    const runnerStatusURL = "/editor/runner/" + runnerUUID + "/";
    fetch(runnerStatusURL).then(function (response) {
      response.json().then(function (runner) {
        console.info(runner);
        updateUI(runner);
        if (runner.status !== "Waiting") {
          clearInterval(runnerInterval);
          stopLoading();
        }
      });
    });
  }, 1000);
}

function updateUI(runner) {
  const output = document.getElementById("output");
  if (runner.status === "TimeoutError") {
    output.value = runner.status;
  } else {
    output.value = runner.output;
  }
}

const loader = document.querySelector(".loader-wrapper");

function startLoading() {
  console.info("Start Loading");
  loader.classList.add("is-active");
}

function stopLoading() {
  console.info("Stoping Loading");
  loader.classList.remove("is-active");
}