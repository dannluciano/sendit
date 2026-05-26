const PORT = process.env.PORT || 8001;

const COOKIE_SECRET = process.env.COOKIE_SECRET || "cookie-secret-random";

const ENV = process.env.ENV || "development";

const DATABASE_URL =
  process.env.DATABASE_URL ||
  "postgres://postgres:postgres@localhost:5432/senditdb";

const SENDIT_LOGIN =
  ENV === "development"
    ? "http://localhost:8000"
    : "http://sendit.dannluciano.com.br";

export default {
  DOCKER_ENGINE_SOCKET: {
    socketPath: "/var/run/docker.sock",
  },
  PORT,
  DATABASE_URL,
  COOKIE_SECRET,
  ENV,
  SENDIT_LOGIN,
};
