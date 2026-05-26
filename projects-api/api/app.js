import * as dockerode from "dockerode";
import { WebSocketServer } from "ws";

import configs from "./configs.js";

import ComputerUnitService from "./computer_unit/computer_unit_service.js";

import setupRoutes from "./routes.js";
import { log } from "./utils.js";
import apiWSConnection from "./websocket/api_websocket.js";
import dockerWSConnection from "./websocket/docker_websocket.js";

const __dirname = new URL("./", import.meta.url).pathname;

let dockerConnection;

log("SERVER", "Current DIR", __dirname);

try {
  log("Connecting to Docker Daemon");
  dockerConnection = new dockerode.default(configs.DOCKER_ENGINE_SOCKET);
  const infos = await dockerConnection.version();
  log(`Docker Daemon Connection Info ${infos.Version}`);
} catch (error) {
  console.error(error);
  console.error("==> Cannot Connect to Docker Daemon!");
  console.error("==> Exiting...");
  process.exit(1);
}

const computeUnitService = new ComputerUnitService(dockerConnection);

const app = setupRoutes(dockerConnection, computeUnitService);

const apiWS = new WebSocketServer({ noServer: true });
const dockerWS = new WebSocketServer({ noServer: true });

function upgradeToWebSocket(request, socket, head) {
  const url = new URL(request.url, "https://example.org/");

  if (url.pathname.match("^/containers/(.*)$")) {
    dockerWS.handleUpgrade(request, socket, head, function done(ws) {
      dockerWS.emit("connection", ws, request);
    });
  } else if (url.pathname.startsWith("/vmws")) {
    apiWS.handleUpgrade(request, socket, head, function done(ws) {
      apiWS.emit("connection", ws, request);
    });
  } else {
    socket.destroy();
  }
}

apiWS.on("connection", apiWSConnection(dockerConnection, computeUnitService));
dockerWS.on("connection", dockerWSConnection());

async function handle_signals() {
  console.log("Ctrl-C was pressed");
  apiWS.close();
}

process.on("SIGINT", handle_signals);
process.on("SIGTERM", handle_signals);

export { app, upgradeToWebSocket };
