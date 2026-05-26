import Dockerode from "dockerode";

/**
 * @typedef {Object} ComputerUnitJSON
 * @property {string} container-id
 * @property {string} temp-dir-path
 * @property {string} project-id
 */

export default class ComputerUnit {
  /**
   *
   * @param {Dockerode.Container} containerInstance
   * @param {string} tempDirPath
   * @param {string} projectId
   */
  constructor(containerInstance, tempDirPath, projectId, ownerUUID) {
    if (containerInstance) {
      this.id = containerInstance.id;
      this.containerId = containerInstance.id;
      this.containerInstance = containerInstance;
    }
    this.tempDirPath = tempDirPath;
    this.projectId = projectId;
    this.ownerUUID = ownerUUID;
  }

  /**
   * @returns {ComputerUnitJSON}
   */
  toJSON() {
    return {
      "container-id": this.containerId,
      "temp-dir-path": this.tempDirPath,
      "project-id": this.projectId,
      "owner-uuid": this.ownerUUID,
    };
  }
}
