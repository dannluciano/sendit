import fs from "node:fs/promises";

import DB, { WSDB } from "../database.js";
import { log } from "../utils.js";

function openProjectFile(dockerConnection, computeUnitService) {
  return async (c) => {
    try {
      const cid = c.req.param("cid");
      const pathEncoded = c.req.param("pathenc");
      const filename = Buffer.from(pathEncoded, "base64")
        .toString("utf-8")
        .substring(1);
      const containerInfo = await dockerConnection.getContainer(cid).inspect();

      log(
        "OPEN",
        `opening ${filename} on container ${cid} - ${containerInfo.Id}`,
      );

      const cuJSON = DB.get(containerInfo.Id);
      if (cuJSON) {
        const computerUnit = computeUnitService.fromJSON(cuJSON);

        const filepath = `${computerUnit.tempDirPath}/${filename}`;
        const content = await fs.readFile(filepath);

        const ws = WSDB.get(computerUnit.containerId);
        if (ws) {
          log(
            "OPEN",
            `sending content of ${filename} on container ${cid} via websocket`,
          );
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
        return new Response("Ok");
      }
    } catch (error) {
      console.error(error);
      return new Response("File not found", {
        status: 404,
      });
    }
  };
}

export { openProjectFile };
