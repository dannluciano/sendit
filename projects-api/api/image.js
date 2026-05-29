import { fileURLToPath } from 'url';
import path from 'path';

const __filename = fileURLToPath(import.meta.url);
const __dirname = path.dirname(__filename);

import * as dockerode from "dockerode";
import tar from 'tar-fs';

import configs from "./configs.js";
import { log } from "./utils.js";

export default async function buildVMImage(dockerConnection) {
    try {
        log("Build VM Image", "Starting...");

        const context = tar.pack(
            path.join(__dirname, '../docker/vm')
        );

        const stream = await dockerConnection.buildImage(
            context,
            {
                t: 'sendit-vm',
            },
        );
        await new Promise((resolve, reject) => {
            dockerConnection.modem.followProgress(
                stream,
                (err, res) => {
                    if (err) return reject(err);
                    resolve(res);
                },
                (event) => {
                    if (event.stream) {
                        process.stdout.write(event.stream);
                    }

                    if (event.status) {
                        console.log(
                            `[${event.id ?? 'build'}] ${event.status} ${event.progress ?? ''}`
                        );
                    }

                    if (event.error) {
                        console.error('BUILD ERROR:', event.error);
                    }
                }
            );
        });
        log("Build VM Image", "Done");
    } catch (error) {
        console.error(error);
    }
}