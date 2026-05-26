import { serve } from "@hono/node-server";
import { app, upgradeToWebSocket } from "./app.js";
import configs from "./configs.js";
import { log } from "./utils.js";

const server = serve(
  {
    fetch: app.fetch,
    port: configs.PORT,
  },
  (info) => {
    log("SERVER", `Listening on http://localhost:${info.port}`);
  },
);

server.on("upgrade", upgradeToWebSocket);

async function handle_signals() {
  console.log("Ctrl-C was pressed");
  server.close();
}

process.on("SIGINT", handle_signals);
process.on("SIGTERM", handle_signals);
