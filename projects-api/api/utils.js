function log(moduleName, msg, ...args) {
  if (msg) {
    console.info(moduleName, "==>", msg, ...args);
  } else {
    console.info("LOG", "==>", moduleName, ...args);
  }
}

function sleep(ms) {
  return new Promise((resolve) => setTimeout(resolve, ms));
}

function debounce(func, wait, immediate, ...args) {
  let timeout;
  return function () {
    clearTimeout(timeout);
    if (immediate && !timeout) func.apply(this, args);
    timeout = setTimeout(() => {
      timeout = null;
      if (!immediate) func.apply(this, args);
    }, wait);
  };
}

function sortTree(treeChildren = [], type = "directory") {
  const targetArray = [];
  const restArray = [];

  for (let index = 0; index < treeChildren.length; ++index) {
    const pathObj = treeChildren[index];
    if (pathObj.children?.length) {
      sortTree(pathObj.children, type);
    }

    if (pathObj.type === type) targetArray.push(pathObj);
    else restArray.push(pathObj);
  }

  const resultTree = [...targetArray, ...restArray];
  for (let index = 0; index < treeChildren.length; ++index) {
    treeChildren[index] = resultTree[index];
  }

  return resultTree;
}

export { log, sleep, debounce, sortTree };
