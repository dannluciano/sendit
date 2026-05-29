import { fileURLToPath } from 'url';
import { dirname } from 'path';

const __filename = fileURLToPath(import.meta.url);
const __dirname = dirname(__filename);

import * as dockerode from "dockerode";

import configs from "../api/configs.js";
import { log } from "../api/utils.js";

let dockerConnection;

try {
    log("Build VM Image", "Connecting to Docker Daemon");
    dockerConnection = new dockerode.default(configs.DOCKER_ENGINE_SOCKET);

    dockerConnection.buildImage({
        context: `${__dirname}/docker/vm`,
        src: ['Dockerfile',]
    }, { t: 'sendit-vm' }, function (err, response) {
        if (error) {
            log("Error", "Build VM Image");
        }
    });
} catch (error) {
    console.error(error);
    console.error("==> Cannot Connect to Docker Daemon!");
    console.error("==> Exiting...");
    process.exit(1);
}