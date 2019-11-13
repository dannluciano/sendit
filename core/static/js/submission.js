/* eslint-env browser, jquery */
/* global  */

function getSubmissionStatus () {
  const url = window.location.href
  $.ajax(url, {
    success: function (response) {
      console.log(response)
      if (response.status !== 'Waiting') {
        clearInterval(interval)
        document.location.href = response.url || '/'
      }
    }
  })
}

const interval = setInterval(getSubmissionStatus, 2500)
