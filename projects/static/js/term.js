const terminalTheme = {
  foreground: "#F8F8F2",
  background: "#21222c",
  black: "#282A36",
  brightBlack: "#4D4D4D",
  red: "#FF5555",
  brightRed: "#FF6E67",
  green: "#50FA7B",
  brightGreen: "#5AF78E",
  yellow: "#F1FA8C",
  brightYellow: "#F4F99D",
  blue: "#BD93F9",
  brightBlue: "#CAA9FA",
  magenta: "#FF79C6",
  brightMagenta: "#FF92D0",
  cyan: "#8BE9FD",
  brightCyan: "#9AEDFE",
  white: "#BFBFBF",
  brightWhite: "#E6E6E6",
};

let globalTerm = null;

class Term {
  constructor() {
    this.terminalElement = document.getElementById("terminal");
    this.term = new Terminal({
      theme: terminalTheme,
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
