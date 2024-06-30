const host = document.location.host;
const hProtocol = document.location.protocol;
const sProtocol = hProtocol === "http:" ? "" : "s";
const currentURL = new URL(document.location);
const debugIsActive = currentURL.searchParams.has("debug");
const testIsActive = currentURL.searchParams.has("test");
const filesystemSection = document.getElementById("filesystem");
const editorTermSection = document.getElementById("editor-term-section");
const filenameDialog = document.getElementById("filename-dialog");
const loadingDialog = document.getElementById("loading-dialog");
const apiURL =
	host === "localhost:8000"
		? "localhost:8001"
		: "ide.sendit.dannluciano.com.br";

let containerId;
let editor;
let apiSocket;
let containerSocket;
const openedFiles = [];
let currentOpenTab = -1;
let term;
let newFileOrNewFolder;
let initialCommand = "";
let settings = {};

if (currentURL.searchParams.has("command")) {
	initialCommand = currentURL.searchParams.get("command");
}

if (isOnMobile()) {
	editorTermSection.classList.add("hidden");
}

function debug(...args) {
	if (debugIsActive) {
		console.log(args);
	}
}

const debounce = (callback, wait) => {
	let timeoutId = null;
	return (...args) => {
		window.clearTimeout(timeoutId);
		timeoutId = window.setTimeout(() => {
			callback.apply(null, args);
		}, wait);
	};
};

function terminalResize() {
	if (apiSocket && term) {
		term.fit();
		apiSocket.send(
			JSON.stringify({
				type: "resize",
				params: term.getDimensions(),
			}),
		);
	}
}

function getScreenOrientation() {
	return window.screen.height > window.screen.width ? "portrait" : "landscape";
}

function isOnMobile() {
	return window.screen.width <= 991;
}

function changeOrientatationOfDevice(event) {
	debug(getScreenOrientation(), isOnMobile(), event);

	setTimeout(terminalResize, 1000);
}

window.addEventListener("resize", debounce(terminalResize, 1000));
window.addEventListener("orientationchange", changeOrientatationOfDevice);

CodeMirror.modeURL = "/assets/vendor/codemirror/mode/%N/%N.js";

function getExtensionIcon(filename, style) {
	const iconFileStylePattern =
		'style="padding-top: 0.4rem; margin-right: 0.5rem"';
	const iconFileLabels = {
		py: "logo-python",
		js: "logo-javascript",
		mjs: "logo-javascript",
		java: "cafe",
		html: "logo-html5",
		file: "document",
		c: "skull",
		cpp: "skull",
		sql: "server",
		scratch: "document",
		sqlite: "file-tray-stacked",
		Dockerfile: "logo-docker",
		dockerignore: "logo-docker",
		Makefile: "construct",
		gitignore: "git-network",
		config: "settings",
		conf: "settings",
		md: "book",
	};
	const extension = getFileExtension(filename);
	let iconName = iconFileLabels.file;
	try {
		iconName = iconFileLabels[extension] || "document";
		if (filename === "package.json" || filename === "package-lock.json") {
			iconName = "logo-npm";
		}
		if (filename === "docker-compose.yml") {
			iconName = "logo-docker";
		}
	} catch (error) {
		const iconName = "bug";
		return `<ion-icon ${
			style ? iconFileStylePattern : null
		} name="${iconName}"></ion-icon>`;
	}
	return `<ion-icon ${
		style ? iconFileStylePattern : null
	} name="${iconName}"></ion-icon>`;
}

function getFolderIcon(foldername) {
	const iconFolderLabels = {
		".github": "logo-github",
		".git": "git-network",
		"folder-open": "folder-open",
	};
	const iconName = iconFolderLabels[foldername] || "folder";
	return iconName;
}

function getFileExtension(fileNameOrPath) {
	return fileNameOrPath.split(".").pop();
}

function getEditorConfigsAndModeWithFileExtension(fileExtention) {
	const defaultOptions = {
		theme: "dracula",
		lineNumbers: true,
		indentUnit: 4,
		matchBrackets: true,
		styleActiveLine: true,
		viewportMargin: 25,
		readOnly: false,
		lineWrapping: true,
	};
	const fileConfigsAndExtentionModes = {
		py: {
			...defaultOptions,
			mode: {
				name: "python",
				version: 3,
				singleLineStringErrors: false,
			},
			indentUnit: 2,
			smartIndent: true,
			tabSize: 2,
			indentWithTabs: false,
		},
		js: {
			...defaultOptions,
			mode: {
				name: "javascript",
			},
		},
		mjs: {
			...defaultOptions,
			mode: {
				name: "javascript",
			},
		},
		json: {
			...defaultOptions,
			indentUnit: 2,
			mode: {
				name: "javascript",
				json: true,
			},
		},
		java: {
			...defaultOptions,
			mode: "text/x-java",
		},
		cpp: {
			...defaultOptions,
			mode: "text/x-c++src",
		},
		c: {
			...defaultOptions,
			mode: "text/x-csrc",
		},
		sql: {
			...defaultOptions,
			mode: "text/x-sqlite",
		},
		scratch: {
			...defaultOptions,
			mode: "properties",
			readOnly: true,
		},
		sqlite: {
			...defaultOptions,
			readOnly: true,
		},
		txt: {
			...defaultOptions,
		},
		html: {
			...defaultOptions,
			mode: "text/html",
		},
		css: {
			...defaultOptions,
			mode: "css",
		},
		yml: {
			...defaultOptions,
			mode: "text/x-yaml",
		},
		sh: {
			...defaultOptions,
			mode: "text/x-sh",
		},
		md: {
			...defaultOptions,
			mode: "text/x-markdown",
			highlightFormatting: true,
		},
		Dockerfile: {
			...defaultOptions,
			mode: "dockerfile",
		},
		config: {
			...defaultOptions,
			mode: "properties",
		},
		conf: {
			...defaultOptions,
			mode: "properties",
		},
	};
	try {
		return (
			fileConfigsAndExtentionModes[fileExtention] || {
				...defaultOptions,
				mode: "properties",
				readOnly: false,
			}
		);
	} catch (error) {
		console.error(error);
		return;
	}
}

function changeEditorConfigsAndMode(filename) {
	const fileExtension = getFileExtension(filename);
	const options = getEditorConfigsAndModeWithFileExtension(fileExtension);
	const extension = CodeMirror.findModeByExtension(fileExtension);
	if (extension) {
		CodeMirror.autoLoadMode(editor, extension);
	}
	debug("changeEditorConfigsAndMode", fileExtension, options, extension);
	for (const key in options) {
		debug(`editor.setOption('${key}', ${options[key]});`);
		editor.setOption(`${key}`, options[key]);
	}
	if (options.readOnly) {
		editor.setValue("");
	}
}

function getRunCommandsWithFileExtensionAndFilepath(fileExtention, filepath) {
	debug(filepath);
	const runCommandsPerLanguages = {
		py: [`python3 ${filepath}\n`],
		js: [`node ${filepath}\n`],
		mjs: [`node ${filepath}\n`],
		json: [],
		java: [`java ${filepath}\n`],
		cpp: [`g++ -o main ${filepath}\n`, "./main"],
		c: [`g++ -o main ${filepath}\n`, "./main"],
		sql: [`cat ${filepath} | sqlite3 db.sqlite \n`],
		scratch: [],
		txt: [],
		html: ["python3 -m http.server -b $HOST $PORT \n"],
		css: ["python3 -m http.server -b $HOST $PORT \n"],
		sqlite3: [`sqlite3 ${filepath}\n`],
		sh: [`bash ${filepath}\n`],
		Makefile: [`make -f ${filepath}\n`],
	};
	try {
		const commands = ["\x03\n", ...runCommandsPerLanguages[fileExtention]];

		if (filepath.includes("requirements.txt")) {
			commands.push("test ! -d env && python3 -m venv env\n");
			commands.push("test -d env && source env/bin/activate\n");
			commands.push(
				`test -f requirements.txt && python -m pip install -r ${filepath}\n`,
			);
		}
		if (filepath.includes("manage.py")) {
			commands.pop();
			commands.push("test ! -d env && python3 -m venv env\n");
			commands.push("test -d env && source env/bin/activate\n");
			commands.push(
				"test -f requirements.txt && python -m pip install -r requirements.txt\n",
			);
			commands.push(`python ${filepath} runserver $HOST:$PORT\n`);
		}
		if (filepath.includes("package.json")) {
			commands.push("npm install\n");
			commands.push("npm start\n");
		}
		if (filepath.includes(".db.json")) {
			commands.push(`npx --yes json-server ${filepath}\n`);
		}

		return commands;
	} catch (error) {
		console.error(error);
		return [];
	}
}

function runCurrentOpenedFile() {
	const file = openedFiles[currentOpenTab];
	const extension = getFileExtension(file.filename);

	saveFile();

	const filepathWithOutHomePath = file.filepath.replace(`${tempDirPath}/`, "");

	const commands = getRunCommandsWithFileExtensionAndFilepath(
		extension,
		filepathWithOutHomePath,
	);
	debug(commands);
	for (const command of commands) {
		containerSocket.send(command);
	}
}

function createNewFileOrFolder(event) {
	if (event.key === "Enter") {
		const filenameField = document.getElementById("input-filename");
		if (newFileOrNewFolder === "file") {
			const filename = filenameField.value;
			const filepath = `${tempDirPath}/${filename}`;
			writeFile(filepath, "");
			openFile(filepath);
		} else {
			const foldername = filenameField.value;
			const folderpath = `${tempDirPath}/${foldername}`;
			makeFolder(folderpath);
		}
		filenameField.value = "";
		filenameDialog.close();
	}
}

document.addEventListener("DOMContentLoaded", () => {
	loadSettings();
	editor = CodeMirror.fromTextArea(document.querySelector("#editor"));
	// editor.setSize("280px", "100%");
	editor.setOption("extraKeys", {
		"Ctrl-S": (cm) => {
			saveFile();
		},
		"Cmd-S": (cm) => {
			saveFile();
		},
		"Ctrl-R": (cm) => {
			runCurrentOpenedFile();
		},
		"Cmd-R": (cm) => {
			runCurrentOpenedFile();
		},
	});
	editor.on("changes", () => {
		if (currentOpenTab >= 0) {
			const fileWasChanged = openedFiles[currentOpenTab].changed;
			openedFiles[currentOpenTab].changed = true;
			if (!fileWasChanged) {
				requestAnimationFrame(renderFilesTabs);
			}
		}
	});
	changeEditorConfigsAndMode("scratch");

	const filenameField = document.getElementById("input-filename");
	filenameField.addEventListener(
		"keypress",
		debounce(createNewFileOrFolder, 250),
	);

	const newFileButton = document.getElementById("new-file-button");
	newFileButton.addEventListener("click", () => {
		newFileOrNewFolder = "file";
		filenameField.placeholder = "File Name (doc.txt)";
		filenameField.style.display = "block";
		filenameDialog.showModal();
		filenameField.focus();
	});

	const newFolderButton = document.getElementById("new-folder-button");
	newFolderButton.addEventListener("click", () => {
		newFileOrNewFolder = "folder";
		filenameField.placeholder = "Folder Name (src/core)";
		filenameField.style.display = "block";
		filenameDialog.showModal();
		filenameField.focus();
	});

	const runButton = document.getElementById("run-button");
	runButton.addEventListener("click", runCurrentOpenedFile);

	const saveButton = document.getElementById("save-button");
	saveButton.addEventListener("click", saveFile);

	const duplicateButton = document.getElementById("duplicate-button");
	duplicateButton.addEventListener("click", duplicateProject);

	const downloadButton = document.getElementById("download-button");
	downloadButton.addEventListener("click", downloadProject);

	const settingsButton = document.getElementById("settings-button");
	settingsButton.addEventListener("click", openOrCloseSettings);

	const saveSettingsButton = document.getElementById("save-settings-button");
	saveSettingsButton.addEventListener("click", saveSettings);

	const cancelSettingsButton = document.getElementById(
		"cancel-settings-button",
	);
	cancelSettingsButton.addEventListener("click", openOrCloseSettings);

	const settingsForm = document.getElementById("settings-form");
	const settingsFormData = new FormData(settingsForm);
	const settingsJSON = formDataToJSON(settingsFormData);
	const settingsJSONString = JSON.stringify(settingsJSON);

	document.addEventListener(
		"keyup",
		(event) => {
			if (event.ctrlKey) {
				if (event.key === "s") saveFile();
				if (event.key === "r") runCurrentOpenedFile();
			}
			if (event.metaKey) {
				if (event.key === "s") saveFile();
				if (event.key === "r") runCurrentOpenedFile();
			}
		},
		false,
	);

	fetch(`${hProtocol}//${apiURL}/api/container/create/`, {
		method: "POST",
		body: `{ "project": ${projectString}, "settings": ${settingsJSONString}}`,
	})
		.then((res) => res.json())
		.then((data) => afterContainerCreation(data))
		.catch((error) => {
			console.error(error);
			const messagesDialog = document.getElementById("messages-dialog");
			messagesDialog.showModal();
		});
	renderFilesTabs();
});

function afterContainerCreation(data) {
	containerId = data["container-id"];
	tempDirPath = data["temp-dir-path"];
	ownerUUID = data["owner-uuid"];

	if (!containerId) return;

	tryExecuteFunctionInLoopWithDelay(connectToContainerWS);
}

function connectToContainerWS() {
	try {
		const containerURL = `ws${sProtocol}://${apiURL}/containers/${containerId}/attach/ws?logs=true&stream=true&stdin=true&stdout=true`; //&stderr=true
		containerSocket = new WebSocket(containerURL);
		containerSocket.onopen = () => {
			term = new Term();
			term.attach(containerSocket);
			debug(containerSocket);

			connectToApiWS();

			if (initialCommand) {
				containerSocket.send(`${initialCommand}\n`);
			}
		};

		containerSocket.onclose = (code, reason) => {
			apiSocket.close();
			term.close();
			debug("Containet WebSocket Disconnected:", code, reason);
		};
		containerSocket.onerror = (err) => {
			apiSocket.close();
			term.close();
			console.error(err);
		};
	} catch (error) {
		console.error(error);
	}
}

function connectToApiWS() {
	try {
		const apiWSURL = `ws${sProtocol}://${apiURL}/vmws?cid=${containerId}`;
		apiSocket = new WebSocket(apiWSURL);
		apiSocket.onopen = () => {
			debug("API WebSocket Connection Opened");
			setTimeout(() => {
				terminalResize();
				loaded();
			}, 100);

			if (testIsActive) {
				createTestFiles();
			}
		};
		debug(apiSocket);

		apiSocket.onclose = (code, reason) => {
			debug("API WebSocket Disconnected:", code, reason);
		};
		apiSocket.onerror = (err) => {
			console.error(err);
		};

		apiSocket.addEventListener("message", (event) => {
			const { type, params } = JSON.parse(event.data);
			if (type === "fs") {
				renderFileSystemTree(params);
			}
			if (type === "host-port") {
				const hostPort = params;
				const shareLink = document.getElementById("open-new-tab");
				const hostName = host.startsWith("localhost")
					? "localhost"
					: "62.72.9.104";
				shareLink.href = `http://${hostName}:${hostPort}`;
			}
			if (type === "open") {
				const { filename, filepath, content } = params;

				const fileIsOpened = openedFiles.findIndex(
					(file) => file.filepath === filepath,
				);

				let file;

				if (fileIsOpened === -1) {
					file = {
						filename,
						filepath,
						changed: false,
						doc: new CodeMirror.Doc(content),
					};
					openedFiles.push(file);
				} else {
					file = openedFiles[fileIsOpened];
				}

				changeCurrentOpenedTabWithFile(file);

				renderFilesTabs();
				editor.focus();
			}
		});
		loadingDialog.close();
	} catch (error) {
		console.error(error);
	}
}

function duplicateProject() {
	fetch(`/api/project/duplicate/${project.uuid}`, {
		method: "POST",
	})
		.then((res) => res.json())
		.then((data) => {
			window.location.pathname = data.path;
		})
		.catch((error) => console.error(error));
}

function downloadProject() {
	fetch(`/public/project/download/${project.uuid}`, {
		method: "POST",
	})
		.then((res) => res.blob())
		.then((blob) => {
			const file = window.URL.createObjectURL(blob);
			const elm = document.createElement("a");
			elm.href = file;
			elm.setAttribute("download", "project.zip");
			elm.click();
		})
		.catch((error) => console.error(error));
}

function saveFile() {
	if (currentOpenTab >= 0 && openedFiles.length > 0) {
		const file = openedFiles[currentOpenTab];
		writeFile(file.filepath, editor.getValue());
		const fileWasChanged = openedFiles[currentOpenTab].changed;
		openedFiles[currentOpenTab].changed = false;
		if (fileWasChanged) {
			renderFilesTabs();
		}
	}
}

function setOpenFile(event) {
	const clickItem = event.target.textContent;
	const files = document.querySelectorAll(".file-item");

	for (let i = 0; i < files.length; i++) {
		const current = files[i];
		if (current.querySelector(".file-item-name").textContent === clickItem) {
			closeFileStyle();
			current.classList.add("file-open");
			break;
		}
	}
}

function setActionFileStyle(text, close) {
	const files = document.querySelectorAll(".file-item");

	debug(text);

	for (let i = 0; i < files.length; i++) {
		const current = files[i];
		if (current.querySelector(".file-item-name").textContent === text) {
			if (close) {
				current.classList.remove("file-open");
			} else {
				current.classList.add("file-open");
			}
			break;
		}
	}
}

function closeFileStyle() {
	const element = document.querySelector(".file-open");

	if (element) {
		element.classList.remove("file-open");
	}
}

function renderFilesTabs() {
	const tabs = document.getElementById("tabs");
	tabs.replaceChildren();

	if (openedFiles.length === 0) {
		const filenameSpan = document.createElement("span");
		filenameSpan.textContent = "scratch";
		filenameSpan.style = "";

		const extensionIcon = document.createElement("span");
		extensionIcon.innerHTML = getExtensionIcon(filenameSpan.textContent);
		extensionIcon.style = "";

		const closeSpan = document.createElement("span");
		closeSpan.innerHTML = '<ion-icon name="close-circle"></ion-icon>';
		closeSpan.onclick = closeTab;
		closeSpan.style = "";

		const p = document.createElement("a");
		p.appendChild(extensionIcon);
		p.appendChild(filenameSpan);
		p.appendChild(closeSpan);

		const li = document.createElement("li");
		li.appendChild(p);
		li.classList.add("is-active");
		tabs.appendChild(li);

		closeFileStyle();
		editor.setValue("");
		editor.setOption("readOnly", true);
		return;
	}

	let fileindex = 0;
	for (const file of openedFiles) {
		const filenameSpan = document.createElement("span");
		filenameSpan.classList.add("file-name-span");

		filenameSpan.textContent = file.changed
			? `${file.filename} * `
			: file.filename;
		filenameSpan.onclick = changeCurrentOpenedTab;
		filenameSpan.dataset.fileindex = fileindex;
		filenameSpan.style = "";

		const extensionIcon = document.createElement("span");
		extensionIcon.innerHTML = getExtensionIcon(file.filename);
		extensionIcon.style = "";

		const closeSpan = document.createElement("span");
		closeSpan.innerHTML = '<ion-icon name="close-circle"></ion-icon>';
		closeSpan.onclick = closeTab;
		closeSpan.dataset.fileindex = fileindex;
		closeSpan.style = "";

		const p = document.createElement("a");
		p.appendChild(extensionIcon);
		p.appendChild(filenameSpan);
		p.appendChild(closeSpan);

		const li = document.createElement("li");
		li.appendChild(p);
		li.onclick = setOpenFile;
		li.dataset.filepath = file.filepath;
		if (currentOpenTab === fileindex) {
			li.classList.add("is-active");
		}
		tabs.appendChild(li);
		fileindex++;
	}
}

function changeCurrentOpenedTab(event) {
	const tabindex = Number.parseInt(event.target.dataset.fileindex);
	const file = openedFiles[tabindex];
	const filepath = file.filepath;

	openFile(filepath);
}

function changeCurrentOpenedTabWithFile(file) {
	closeFileStyle();
	setActionFileStyle(file.filename, false);

	const tabindex = openedFiles.findIndex(
		(currentFile) => currentFile.filepath === file.filepath,
	);
	editor.swapDoc(file.doc);
	changeEditorConfigsAndMode(file.filename);
	currentOpenTab = tabindex;
	renderFilesTabs();
}

function closeTab(event) {
	const element =
		event.target.parentNode.parentNode.querySelector(".file-name-span");
	if (element) {
		setActionFileStyle(element.textContent, true);
	}

	const tabindex = Number.parseInt(event.target.parentNode.dataset.fileindex);
	openedFiles.splice(tabindex, 1);
	if (openedFiles.length === 0) {
		currentOpenTab = -1;
	} else {
		changeCurrentOpenedTabWithFile(openedFiles[openedFiles.length - 1]);
	}

	renderFilesTabs();
}

function renderFileSystemTree(data) {
	const filesystem = document.querySelector("#file-system-tree");

	filesystem.replaceChildren();

	for (const child of data.children) {
		if ("children" in child) {
			filesystem.appendChild(renderFolder(child));
		} else {
			filesystem.appendChild(renderFile(child));
		}
	}
}

function renderFolder(folder) {
	const summary = document.createElement("summary");
	const div = document.createElement("div");
	div.classList.add("drac-text", "drac-text-green");
	div.setAttribute("onclick", "toggleFolderIcon(this)");
	const folderIcon = getFolderIcon(folder.name);
	div.innerHTML = `<ion-icon class="filesystem-folder-icon" name="${folderIcon}"></ion-icon>`;
	const span = document.createElement("span");
	span.textContent = folder.name;

	div.appendChild(span);
	summary.appendChild(div);

	const files = document.createElement("ul");

	for (const child of folder.children) {
		if ("children" in child) {
			files.appendChild(renderFolder(child));
		} else {
			files.appendChild(renderFile(child));
		}
	}

	const details = document.createElement("details");
	details.appendChild(summary);
	details.appendChild(files);

	const li = document.createElement("li");
	li.dataset.path = folder.path;
	li.appendChild(details);

	return li;
}

function renderFile(child) {
	const li = document.createElement("li");
	li.classList.add("file-item");
	const div = document.createElement("div");
	div.innerHTML = getExtensionIcon(child.name, false);
	const span = document.createElement("span");
	span.textContent = child.name;
	span.classList.add("file-item-name");
	div.appendChild(span);
	li.appendChild(div);

	span.dataset.path = child.path;
	span.onclick = openFileInTree;
	return li;
}

function logOut(event) {
	event.preventDefault();
	fetch("/logout", {
		method: "POST",
		headers: {
			"Content-Type": "application/json",
		},
	})
		.then((res) => {
			return res.json();
		})
		.then((data) => {
			if (data.redirect_to) {
				window.location = data.redirect_to;
			}
		})
		.catch((error) => {
			console.error(error);
		});
}

function openOrCloseSettings(event) {
	event.preventDefault();
	const settingsDialog = document.getElementById("settings-dialog");
	if (settingsDialog.open) {
		settingsDialog.close();
	} else {
		settingsDialog.showModal();
	}
}

function saveSettings(event) {
	event.preventDefault();
	const settingsForm = document.getElementById("settings-form");
	const settingsFormData = new FormData(settingsForm);
	const settings = formDataToJSON(settingsFormData);
	const settingsJSONString = JSON.stringify(settings);
	localStorage.setItem("settings", settingsJSONString);
	window.location.reload(true);
}

function loadSettings() {
	const settingsJSONString = localStorage.getItem("settings") || "{}";
	settings = JSON.parse(settingsJSONString);
	debug(settings);
	const settingsFormData = new FormData();
	for (const [key, value] of Object.entries(settings)) {
		settingsFormData.append(key, value);
	}
	debug(settingsFormData);
	const settingsForm = document.getElementById("settings-form");
	formDataToForm(settingsForm, settingsFormData);
}

function openFileInTree(event) {
	const filepath = event.target.dataset.path;
	openFile(filepath);

	if (isOnMobile()) {
		toggleFilesystemSidebar();
	}
}

function openFile(filepath) {
	apiSocket.send(
		JSON.stringify({
			type: "open",
			params: {
				filepath: filepath,
			},
		}),
	);
}

function writeFile(filepath, source) {
	if (!apiSocket) {
		return;
	}

	apiSocket.send(
		JSON.stringify({
			type: "writeInPath",
			params: {
				filepath,
				source,
				ownerUUID,
			},
		}),
	);
}

function makeFolder(folderpath) {
	if (!apiSocket) {
		return;
	}

	apiSocket.send(
		JSON.stringify({
			type: "mkdir",
			params: {
				folderpath,
			},
		}),
	);
}

function loaded() {
	if (!apiSocket) {
		return;
	}

	apiSocket.send(
		JSON.stringify({
			type: "loaded",
			params: {},
		}),
	);
}

function sendControl(element) {
	const mapKey = {
		C: 67,
		D: 68,
		L: 76,
		Z: 90,
	};
	const key = element.dataset.key || "";
	const input = document.getElementsByClassName("xterm-helper-textarea")[0];
	const keyboard = Keysim.Keyboard.US_ENGLISH;
	const ctrlKey = new Keysim.Keystroke(Keysim.Keystroke.CTRL, mapKey[key]);
	keyboard.dispatchEventsForKeystroke(ctrlKey, input);
	debug(`CTRL${mapKey[key]}`);
}

function sendTab(element) {
	containerSocket.send("\t");
	debug("TAB");
}

function createTestFiles() {
	let file = {
		filename: "index.mjs",
		filepath: `${tempDirPath}/index.mjs`,
		changed: false,
		doc: new CodeMirror.Doc(`
import { createServer } from 'node:http';

const server = createServer((req, res) => {
  res.writeHead(200, { 'Content-Type': 'text/plain' });
  res.end('Hello World!');
});

// starts a simple http server locally on port 8080
server.listen(8080, '0.0.0.0', () => {
  console.log('Listening on 0.0.0.0:8080');
});
`),
	};
	openedFiles.push(file);

	currentOpenTab = openedFiles.length - 1;
	changeCurrentOpenedTabWithFile(file);
	saveFile();

	file = {
		filename: "package.json",
		filepath: `${tempDirPath}/package.json`,
		changed: false,
		doc: new CodeMirror.Doc(`{
  "name": "${project.name}",
  "version": "1.0.0",
  "description": "",
  "main": "index.mjs",
  "scripts": {
    "start": "nodejs index.mjs"
  },
  "keywords": [],
  "author": "",
  "license": "ISC"
}`),
	};
	openedFiles.push(file);

	currentOpenTab = 2;
	changeCurrentOpenedTabWithFile(file);
	saveFile();
}

const script = document.createElement("script");
script.src = "/assets/vendor/keysim/keysim.js";
document.body.appendChild(script);

function tryExecuteFunctionInLoopWithDelay(
	func,
	numAttempts = 5,
	delayMs = 100,
	...args
) {
	const sleep = (ms) => {
		const start = Date.now();
		while (Date.now() - start < ms) {}
	};

	const attempt = (i) => {
		try {
			console.log(`Attempt ${i}: ${func.name}`);
			if (typeof func === "function") {
				return func(...args);
			}
			throw new Error("Provided argument is not a function");
		} catch (error) {
			console.error(
				`An error occurred during function execution in attempt ${i}:`,
				error.message,
			);
			if (i < numAttempts) {
				console.log(
					`Waiting for ${delayMs} milliseconds before next attempt...`,
				);
				sleep(delayMs);
				return attempt(i + 1);
			}
		}
	};

	return attempt(1);
}

function formDataToJSON(formData) {
	const object = {};
	formData.forEach((value, key) => {
		// Reflect.has in favor of: object.hasOwnProperty(key)
		if (!Reflect.has(object, key)) {
			object[key] = value;
			return;
		}
		if (!Array.isArray(object[key])) {
			object[key] = [object[key]];
		}
		object[key].push(value);
	});
	return object;
}

function formDataToForm(form, data) {
	for (const [key, val] of new URLSearchParams(data).entries()) {
		const input = form.elements[key];
		if (input) {
			if (input.type === "checkbox") {
				input.checked = !!val;
			} else {
				input.value = val;
			}
		}
	}
}

function closeDialog(element) {
	element.parentNode.close();
}

function toggleFolderIcon(element) {
	const icon = element.querySelector(".filesystem-folder-icon");
	const foldername =
		element.parentElement.parentElement.parentElement.dataset.path
			.split("/")
			.pop() || "folder";
	if (icon.getAttribute("name") === "folder") {
		const folderIcon = getFolderIcon("folder-open");
		icon.setAttribute("name", folderIcon);
	} else {
		const folderIcon = getFolderIcon(foldername);
		icon.setAttribute("name", folderIcon);
	}
}

function toggleFilesystemSidebar() {
	const filesystem = document.querySelector("#filesystem-section");

	const fileTrayIcon = document.getElementById("file-tray-icon");

	if (filesystem.classList.contains("hidden")) {
		if (!isOnMobile()) {
			document.documentElement.style.setProperty("--filesystem-width", "30vw");
		} else {
			document.documentElement.style.setProperty("--filesystem-width", "80vw");
		}

		filesystem.classList.toggle("hidden");
		fileTrayIcon.name = "file-tray";
	} else {
		document.documentElement.style.setProperty("--filesystem-width", "0vw");
		filesystem.classList.toggle("hidden");
		fileTrayIcon.name = "file-tray-full";
	}
	if (isOnMobile()) {
		editorTermSection.classList.toggle("hidden");
	}
	terminalResize();
}
