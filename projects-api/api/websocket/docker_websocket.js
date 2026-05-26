import { WebSocket } from "ws";

export default function dockerWSConnection() {
  return async (clientToServerWS, req) => {
    console.info(
      `WebSocket -> Server Connection Opened: ${JSON.stringify(req.url)}`,
    );

    const serverToDockerWS = new WebSocket(
      `ws+unix:///var/run/docker.sock:${req.url}`,
    );
    serverToDockerWS.on("open", () => {
      console.info(
        `WebSocket -> Docker Connection Opened: ${JSON.stringify(req.url)}`,
      );
    });

    serverToDockerWS.on("message", async (message) => {
      clientToServerWS.send(message);
    });

    serverToDockerWS.on("close", async function close() {
      console.info(`WebSocket -> Docker Connection closed:`);
    });
    serverToDockerWS.on("error", console.error);

    clientToServerWS.on("message", async (message) => {
      if (serverToDockerWS.readyState === serverToDockerWS.OPEN) {
        serverToDockerWS.send(message);
      }
    });

    clientToServerWS.on("close", async function close() {
      console.info(`WebSocket -> Server Connection closed:`);
    });
    clientToServerWS.on("error", console.error);
  };
}
