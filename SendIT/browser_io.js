const fs = require('fs')

const document = {
  write: function (msg) {
    console.log(msg)
  }
}

function alert (msg) {
  console.log(msg)
}

function prompt (msg) {
  process.stdin.resume()
  var buffer = Buffer.alloc(1)
  var result = ''
  var bytesRead

  while (true) {
    bytesRead = 0
    try {
      bytesRead = fs.readSync(process.stdin.fd, buffer, 0, 1)
    } catch (e) {
      if (e.code === 'EAGAIN') {
        console.error('ERROR: interactive stdin input not supported.')
        process.exit(1)
      } else if (e.code === 'EOF') {
        break
      }
      throw e
    }
    if (bytesRead === 0) {
      break
    }

    var char = buffer.toString('utf8')
    if (char === '\r') {
      continue
    } else if (char === '\n') {
      break
    } else {
      result += char
    }
  }

  process.stdin.pause()
  return result
}

function confirm (msg) {
  const result = prompt()

  if ((result === 'Sim') || (result === 'sim') || (result === 'S') || (result === 's') ||
    (result === 'Yes') || (result === 'yes') || (result === 'Y') || (result === 'y') ||
    (result === 'Ok') || (result === 'ok') || (result === '1')) {
    return true
  } else {
    return false
  }
}
