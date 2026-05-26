import { getSignedCookie } from "hono/cookie";
import configs from "../configs.js";
import { log } from "../utils.js";

export default async function isAuthenticated(c, next) {
  try {
    const sessionID = getSignedCookie(c, configs.COOKIE_SECRET, "sessionid");
    if (sessionID) {
      log("AUTH MIDDLEWARE", "success");
      c.set("user-uuid", sessionID);
      return await next();
    }
    log("AUTH MIDDLEWARE", "failure");
    return c.redirect(configs.SENDIT_LOGIN);
  } catch (error) {
    console.error(error);
    return c.redirect(configs.SENDIT_LOGIN);
  }
}
