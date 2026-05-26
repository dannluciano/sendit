const terminalThemes = {
	"ctp-mocha": {
		foreground: "#cdd6f4",
		background: "#1e1e2e",
		black: "#181825",
		brightBlack: "#11111b",
		red: "#f38ba8",
		brightRed: "#eba0ac",
		green: "#a6e3a1",
		brightGreen: "#94e2d5",
		yellow: "#f9e2af",
		brightYellow: "#fab387",
		blue: "#89b4fa",
		brightBlue: "#b4befe",
		magenta: "#f5c2e7",
		brightMagenta: "#cba6f7",
		cyan: "#89dceb",
		brightCyan: "#74c7ec",
		white: "#bac2de",
		brightWhite: "#a6adc8",
	},
	"ctp-latte": {
		foreground: "#4c4f69",
		background: "#eff1f5",
		black: "#5c5f77",
		brightBlack: "#6c6f85",
		red: "#d20f39",
		brightRed: "#e64553",
		green: "#40a02b",
		brightGreen: "#179299",
		yellow: "#df8e1d",
		brightYellow: "#fe640b",
		blue: "#1e66f5",
		brightBlue: "#04a5e5",
		magenta: "#8839ef",
		brightMagenta: "#7287fd",
		cyan: "#209fb5",
		brightCyan: "#7287fd",
		white: "#e6e9ef",
		brightWhite: "#dce0e8",
	},
};

let globalTerm = null;

document.addEventListener("theme-changed", () => {
	if (!globalTerm) return;

	globalTerm.term.options.theme = terminalThemes[getThemeName()];
});

class Term {
	constructor() {
		this.disposed = false;
		this.terminalElement = document.getElementById("terminal");
		this.term = new Terminal({
			theme: terminalThemes[getThemeName()],
			cursorBlink: true,
			convertEol: true,
			fontSize: 18,
			fontFamily: '"Fira Code", monospace',
		});
		this.fitAddon = new FitAddon.FitAddon();
		this.term.loadAddon(this.fitAddon);
		this.term.open(this.terminalElement);
		globalTerm = this;
		this.xterm_resize_ob = new ResizeObserver(() => {
			try {
				setTimeout(() => {
					if (this.disposed || globalTerm !== this) {
						return;
					}
					debug("ResizeObserver", this);
					this.fit();
					this.refresh();
				}, 100);
			} catch (err) {
				console.log(err);
			}
		});
		this.xterm_resize_ob.observe(this.terminalElement);
		this.term.attachCustomKeyEventHandler((event) => {
			if (event.keyCode === 27) {
				const terminalDialog = document.getElementById("terminal-dialog");
				if (terminalDialog) {
					terminalDialog.togglePopover();
				}
				return false;
			}
			return true;
		});
	}

	fit() {
		if (!this.isRenderable()) {
			return false;
		}
		this.fitAddon.fit();
		this.term.scrollToBottom();
		return true;
	}

	focus() {
		this.term.focus();
	}

	refresh() {
		this.term.refresh(0, this.term.rows - 1)
	}

	attach(containerSocket) {
		this.connection = containerSocket;
		const attachAddon = new AttachAddon.AttachAddon(containerSocket);
		this.term.loadAddon(attachAddon);
		this.fit();
	}

	close() {
		if (this.disposed) {
			return;
		}
	}

	dispose() {
		if (this.disposed) {
			return;
		}
		this.disposed = true;
		this.xterm_resize_ob.disconnect();
		if (this.onKeyDisposable) { this.onKeyDisposable.dispose(); }
		this.term.dispose();
		if (globalTerm === this) {
			globalTerm = null;
		}
	}

	getDimensions() {
		return {
			w: this.term.cols,
			h: this.term.rows,
		};
	}

	isRenderable() {
		return (
			!this.disposed &&
			this.terminalElement &&
			this.terminalElement.clientWidth > 0 &&
			this.terminalElement.clientHeight > 0
		);
	}
}
