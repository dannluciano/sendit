import fs from "node:fs/promises";
import * as path from "node:path";
import { default as directoryTree } from "directory-tree";

import DB, { WSDB } from "../database.js";
import { log, sortTree } from "../utils.js";

export default function apiWSConnection(dockerConnection, computeUnitService) {
  return async (ws, req) => {
    console.info(`API WebSocket Connection Opened: ${JSON.stringify(req.url)}`);

    const containerId = new URL(req.url, "http://localhost").searchParams.get(
      "cid",
    );

    let computerUnit;
    const cuJSON = DB.get(containerId);
    if (cuJSON) {
      computerUnit = computeUnitService.fromJSON(cuJSON);
    } else {
      console.error(`ERROR: Dont find computerUnit with id: ${containerId}`);
      return;
    }

    computerUnit.ws = ws;

    WSDB.set(computerUnit.containerId, ws);

    ws.on("message", async (message) => {
      try {
        const cmd = JSON.parse(message);
        if (cmd.type === "resize") {
          const container = dockerConnection.getContainer(containerId);
          await container.resize(cmd.params);
        }
        if (cmd.type === "write") {
          const { filename, source, ownerUUID } = cmd.params;
          const cu = DB.get(containerId);
          if (cu["owner-uuid"] === ownerUUID) {
            const tempDirPath = computerUnit.tempDirPath;
            const path = `${tempDirPath}/${filename}`;
            await fs.writeFile(path, source);
          }
        }
        if (cmd.type === "writeInPath") {
          const { filepath, source, ownerUUID } = cmd.params;
          const cu = DB.get(containerId);
          if (cu["owner-uuid"] === ownerUUID) {
            await fs.writeFile(filepath, source);
          } else {
            ws.send(
              JSON.stringify({
                type: "authorization-error",
                params: {
                  msg: "You is not Owner of Project",
                },
              }),
            );
          }
        }
        if (cmd.type === "mkdir") {
          const { folderpath } = cmd.params;
          await fs.mkdir(folderpath, {
            recursive: true,
          });
        }
        if (cmd.type === "open") {
          const { filepath } = cmd.params;
          const content = await fs.readFile(filepath);
          const filename = path.basename(filepath);

          ws.send(
            JSON.stringify({
              type: "open",
              params: {
                filename,
                filepath,
                content: content.toString("utf-8"),
              },
            }),
          );
        }
        if (cmd.type === "loaded") {
          if (computerUnit.tempDirPath) {
            const tree = directoryTree(computerUnit.tempDirPath, {
              attributes: ["type"],
              exclude:
                /\.npm|\.cache|env|\.node_repl_history|\.vscode|\.sqlite_history/,
            });
            if (tree.children) {
              const sortedChildren = sortTree(tree.children);
              tree.children = sortedChildren;
            }
            ws.send(
              JSON.stringify({
                type: "fs",
                params: tree,
              }),
            );
          }

          const containerInfo = await dockerConnection
            .getContainer(containerId)
            .inspect();
          // log(containerInfo.NetworkSettings);
          const hostPort =
            containerInfo.NetworkSettings.Ports["8080/tcp"][0].HostPort;
          ws.send(
            JSON.stringify({
              type: "host-port",
              params: hostPort,
            }),
          );
        }
      } catch (error) {
        console.error(error);
      }
    });

    ws.on("close", async function close() {
      console.info(`WebSocket Connection closed:`);
      log("Connecting to Docker Daemon");
      try {
        const container = dockerConnection.getContainer(containerId);
        log("Removing Docker ComputerUnit: ", containerId);
        await container.stop();
        // await container.remove()
      } catch (error) {
        if (error.reason === "no such container") return;
        console.error(error);
      }
    });
    ws.on("error", console.error);
  };
}
