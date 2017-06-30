const fs = require('fs')

function alert (msg) {
  console.log(msg)
}

function prompt (msg) {
  process.stdin.resume()
  var buffer = Buffer.alloc(1)
  var result = ''

  do {
    try {
      fs.readSync(process.stdin.fd, buffer, 0, 1, null)
    } catch (e) {
      if (e.code === 'EAGAIN') {
        // 'resource temporarily unavailable'
        // Happens on OS X 10.8.3 (not Windows 7!), if there's no
        // stdin input - typically when invoking a script without any
        // input (for interactive stdin input).
        // If you were to just continue, you'd create a tight loop.
        console.error('ERROR: interactive stdin input not supported.')
        process.exit(1)
      } else if (e.code === 'EOF') {
        // Happens on Windows 7, but not OS X 10.8.3:
        // simply signals the end of *piped* stdin input.
        break
      }
      throw e
    }
    var char = buffer.toString('utf8')
    if (char !== '\r' && char !== '\n') {
      result += char
    } else {
      break
    }
  } while (char !== '\n')

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
