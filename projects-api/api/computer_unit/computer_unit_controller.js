import ComputerUnit from "./computer_unit.js";
import { watchTempDir } from "./temp_dir.js";

import { DB } from "../database.js";

class ComputerUnitController {
  dockerConnection = "";

  constructor(computeUnitService) {
    this.computeUnitService = computeUnitService;
  }

  async createComputerUnit(c) {
    try {
      const payload = await c.req.json();
      const settings = payload.settings;
      const project = payload.project;

      const computerUnit =
        await this.computeUnitService.getOrCreateComputerUnit(
          project,
          settings,
        );

      DB.set(computerUnit.containerId, computerUnit.toJSON());
      DB.set(computerUnit.projectId, computerUnit.toJSON());

      watchTempDir(computerUnit);

      const containerCreateResponse = computerUnit.toJSON();
      return c.json(containerCreateResponse);
    } catch (error) {
      console.error(error);
      return c.json(
        {
          msg: error.msg,
        },
        500,
      );
    }
  }
}

export default ComputerUnitController;
