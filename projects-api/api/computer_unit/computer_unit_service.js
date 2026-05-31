import { log } from "../utils.js";
import ComputerUnit from "./computer_unit.js";
import configs from "../configs.js";
import { getEnvsFromSettings } from "./envs.js";
import { createTempDir } from "./temp_dir.js";

export default class ComputerUnitService {
  constructor(dockerConnection) {
    this.dockerConnection = dockerConnection;
  }

  async getOrCreateComputerUnit(project, settings = {}) {
    try {
      const tempDirPath = await createTempDir(project.temp_dir);

      const envs = getEnvsFromSettings(settings);

      log("CPU", "Creating container");
      const defaultContainerConf = {
        Image: configs.SENDIT_IDE_VM_IMAGE_NAME,
        AttachStdin: false,
        AttachStdout: false,
        AttachStderr: false,
        Tty: true,
        Cmd: ["/bin/bash"],
        Env: envs,
        OpenStdin: true,
        StdinOnce: false,
        WorkingDir: "/root",
        StopTimeout: 2,
        Volumes: {
          "/root": {},
        },
        ExposedPorts: {
          "8080/tcp": {},
        },
        HostConfig: {
          Binds: [`${tempDirPath}:/root`],
          AutoRemove: true,
          PublishAllPorts: true,
          Memory: 512 * 1024 * 1024,

          Ulimits: [
            { Name: "nofile", Soft: 1024, Hard: 1048 },
            { Name: "fsize", Soft: 36 * 1024 * 1024, Hard: 38 * 1024 * 1024 },
          ],
        },
        Labels: {
          "com.docker.instances.service": "vm",
        },
      };
      if (process.env.NODE_ENV === "production") {
        defaultContainerConf.HostConfig.StorageOpt = { size: "2G" };
      }
      const containerInstance =
        await this.dockerConnection.createContainer(defaultContainerConf);

      log("CPU", "Starting container: ", containerInstance.id);
      await containerInstance.start();

      log("CPU", "Return New Container");
      return new ComputerUnit(
        containerInstance,
        tempDirPath,
        project.uuid,
        project.owner_id,
      );
    } catch (error) {
      console.error("Error!", error);
      throw "Error! Cannot create container";
    }
  }

  fromJSON(cuJSON) {
    const containerInstance = this.dockerConnection.getContainer(
      cuJSON["container-id"],
    );
    const tempDirPath = cuJSON["temp-dir-path"];
    const projectId = cuJSON["project-id"];
    const ownerUUID = cuJSON["owner-uuid"];
    return new ComputerUnit(
      containerInstance,
      tempDirPath,
      projectId,
      ownerUUID,
    );
  }

  async removeComputerUnits() {
    const opts = {
      filters: '{"label": ["com.docker.instances.service": "vm"]}',
    };

    try {
      await this.dockerConnection.pruneContainers({
        opts,
      });
    } catch (error) {
      console.error(error);
    }
  }
}
