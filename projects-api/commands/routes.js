import setupRoutes from "../api/routes.js";

import { getRouterName, showRoutes } from "hono/dev";

const app = setupRoutes();

console.info(getRouterName(app));
console.info(showRoutes(app));
