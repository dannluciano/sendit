/* eslint-env browser, jquery */
/* global  */

function getSubmissionStatus() {
	const url = window.location.href;
	$.ajax(url, {
		success: (response) => {
			console.log(response);
			if (response.status !== "Waiting") {
				clearInterval(interval);
				window.history.replaceState(null, "", response.url);
				document.location.href = response.url || "/";
			}
		},
	});
}

const interval = setInterval(getSubmissionStatus, 2500);
