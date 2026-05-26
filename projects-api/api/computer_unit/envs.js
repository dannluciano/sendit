import configs from "../configs.js";

function getEnvsFromSettings(settings) {
  const envsNameFromSettingsMap = {
    name: "GIT_AUTHOR_NAME",
    email: "EMAIL",
    "github-username": "GITHUB_USERNAME",
    "github-auth-token": "GITHUB_TOKEN",
  };
  const envs = [`SENDIT_IDE_ENV=${configs.ENV}`];
  for (const [key, value] of Object.entries(settings)) {
    try {
      const envName = envsNameFromSettingsMap[key];
      envs.push(`${envName}=${value}`);
    } catch (error) {}
  }
  envs.push(`GIT_CONFIG_COUNT=2`);
  envs.push(`GIT_CONFIG_KEY_0=credential.https://github.com.username`);
  envs.push(`GIT_CONFIG_VALUE_0=${settings["github-username"]}`);
  envs.push(`GIT_CONFIG_KEY_1=credential.https://github.com.helper`);
  envs.push(
    `GIT_CONFIG_VALUE_1=!f() { test "$1" = get && echo "password=$(echo $GITHUB_TOKEN)"; }; f`,
  );

  return envs;
}

export { getEnvsFromSettings };
