/* global fetch */

async function setupPyodide() {
  startLoading();
  let pyodide = await loadPyodide({
    indexURL: "https://cdn.jsdelivr.net/pyodide/v0.20.0/full/",
  });
  stopLoading();
  return pyodide;
}

async function evaluatePython(source, debug = false) {
  let pyodide = pythonInstance;
  try {
    await pyodide.runPythonAsync(
      `import sys;import io;sys.stdout = io.StringIO()`
    );
    await pyodide.runPythonAsync(source);
    const stdout = await pyodide.runPythonAsync("sys.stdout.getvalue()");
    return { status: "OK", output: stdout };
  } catch (err) {
    console.error(err);
    return { status: "RuntimeError", output: err };
  }
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
      const csrftoken = document.querySelector(
        "[name=csrfmiddlewaretoken]"
      ).value;

      const code = editor.getValue();
      const lang = languageSelector.value;
      const input = inputField.value;

      if (lang === "null") {
        return;
      }

      startLoading();

      if (lang === "pythonwasm") {
        evaluatePython(code).then(function (runner) {
          updateUI(runner);
          stopLoading();
        });
        return;
      }

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
    output.innerText = runner.status;
  } else {
    output.innerText = runner.output;
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
