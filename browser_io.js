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
      // Read next byte when char is \r or result is empty and char is blank (' ', '\t')
    if (char === '\r' || (result.length === 0 && (char === ' ' || char === '\t'))) {
      continue
    } else if (char === '\n' || char === ' ' || char === '\t') {
      break
    } else {
      result += char
    }
  }

  process.stdin.pause()
  return result
}

function confirm (msg) {
  const result = prompt()[0].toLowerCase()

  return ((result === 't') || (result === 's') || (result === 'y') || (result === '1'))
}
