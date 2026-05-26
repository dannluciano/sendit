import * as fs from "node:fs/promises";
import * as os from "node:os";
import * as path from "node:path";

import * as chokidar from "chokidar";
import { default as directoryTree } from "directory-tree";

import { WSDB } from "../database.js";
import { debounce, log } from "../utils.js";

async function createTempDir(tempDir) {
  log("TMP", "Creating Temp Folder");

  const tempDirPath = `/home/sendit/ide-vm-home-${tempDir}`;
  await fs.mkdir(tempDirPath, { recursive: true });
  log("TMP", `Created Temp Folder: ${tempDirPath}`);
  return tempDirPath;
}

function watchTempDir(computerUnit) {
  try {
    if (!computerUnit.tempDirPath) {
      log("WATCH", `Watching Temp Dir Disable`);
      return;
    }

    function sendFileSystemChanges() {
      const ws = WSDB.get(computerUnit.containerId);
      if (ws) {
        const tree = directoryTree(computerUnit.tempDirPath, {
          exclude: /\.npm|\.cache|env|\.node_repl_history/,
        });
        ws.send(
          JSON.stringify({
            type: "fs",
            params: tree,
          }),
        );
      }
    }

    const sendFileSystemChangesDebouced = debounce(sendFileSystemChanges, 1000);

    log("WATCH", `Watching Temp Dir: ${computerUnit.tempDirPath} Enable`);
    chokidar
      .watch(computerUnit.tempDirPath, {
        ignored: /(^|[\/\\])\..|.cache|env|node_modules/,
        ignoreInitial: true,
      })
      .on("all", (event, path) => {
        sendFileSystemChangesDebouced();
      });
  } catch (error) {
    console.error(error);
  }
}

export { createTempDir, watchTempDir };
