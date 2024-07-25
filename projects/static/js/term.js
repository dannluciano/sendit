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
		this.terminalElement = document.getElementById("terminal");
		this.term = new Terminal({
			theme: terminalThemes[getThemeName()],
		});
		this.term.__connection = "";
		this.fitAddon = new FitAddon.FitAddon();
		this.term.loadAddon(this.fitAddon);
		this.term.open(this.terminalElement);
		this.term.write("\x1B[1;3;31mCarregando...\x1B[0m $ ");
		this.term.onResize((evt) => {
			console.log(evt);
		});
		globalTerm = this;
		this.xterm_resize_ob = new ResizeObserver((entries) => {
			try {
				// console.log(entries)
				globalTerm.fit();
			} catch (err) {
				console.log(err);
			}
		});
		this.xterm_resize_ob.observe(this.terminalElement);
	}
	fit() {
		debug("Term Resize");
		this.fitAddon.fit();
		this.term.scrollToBottom();
	}

	attach(containerSocket) {
		this.connection = containerSocket;
		const attachAddon = new AttachAddon.AttachAddon(containerSocket);
		this.term.loadAddon(attachAddon);
		this.fit();
		this.term.reset();
		this.term.paste("clear\n");
	}

	close() {
		this.term.reset();
		this.term.writeln("Disconnected");
	}

	getDimensions() {
		return {
			w: this.term.cols,
			h: this.term.rows,
		};
	}
}
