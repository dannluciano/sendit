import * as dockerode from "dockerode";

import configs from "../api/configs.js";
import { log } from "../api/utils.js";

let dockerConnection;

try {
  log("Remove Unused Containers", "Connecting to Docker Daemon");
  dockerConnection = new dockerode.default(configs.DOCKER_ENGINE_SOCKET);

  const containers = await dockerConnection.listContainers({
    filters: {
      label: ["com.docker.instances.service=vm"],
    },
  });

  const now = new Date();
  log("NOW: ", now);

  for await (const containerInfo of containers) {
    const container = await dockerConnection.getContainer(containerInfo.Id);
    // const psout = await container.top({ ps_args: "aux" });
    const psout = await container.top();
    const promises = [];
    if (psout.Processes.length === 1) {
      const containerInspect = await container.inspect();
      const startedAt = new Date(containerInspect.State.StartedAt);
      const diff = Math.abs(now - startedAt);
      if (diff > 1000 * 60 * 30) {
        promises.push(container.stop());
        log(
          "",
          `Removing Container ${containerInfo.Id} started at: ${startedAt}`,
        );
      }
    }
    Promise.all(promises);
  }
} catch (error) {
  console.error(error);
  console.error("==> Cannot Connect to Docker Daemon!");
  console.error("==> Exiting...");
  process.exit(1);
}
