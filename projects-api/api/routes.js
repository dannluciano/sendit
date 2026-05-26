import { Hono } from "hono";
import { cors } from "hono/cors";
import { logger } from "hono/logger";

import isAuthenticated from "./auth/auth_middleware.js";
import ComputerUnitController from "./computer_unit/computer_unit_controller.js";
import { openProjectFile } from "./projects/projects_controller.js";

function setupRoutes(dockerConnection, computeUnitService) {
  const computerUnitController = new ComputerUnitController(computeUnitService);
  const app = new Hono();

  app.use("/api/*", logger());
  app.use("/api/*", isAuthenticated);
  app.use("/api/*", cors());

  app.get(
    "/api/fs/file/open/:cid/:pathenc",
    openProjectFile(dockerConnection, computeUnitService),
  );

  app.post(
    "/api/container/create/",
    computerUnitController.createComputerUnit.bind(computerUnitController),
  );

  app.get("/version", async (c) => {
    return c.text("v0.0.1");
  });

  return app;
}

export default setupRoutes;
