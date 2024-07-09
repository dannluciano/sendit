/* eslint-env browser, jquery */

const lightThemeName = "light";
const darkThemeName = "dark";

function init() {
	const theme = getTheme();

	applayTheme(theme);
	setTheme(theme);
}

function setTheme(theme) {
	localStorage.setItem("theme", theme);
}

function getTheme() {
	return localStorage.getItem("theme") || lightThemeName;
}

function applayTheme(theme) {
	document.body.dataset.theme = theme;
}

function darkxlight() {
	const element = document.body;
	const fromTheme = element.dataset.theme;
	let toTheme = fromTheme;

	if (fromTheme === lightThemeName) {
		toTheme = darkThemeName;
	} else {
		toTheme = lightThemeName;
	}

	console.info("Change Theme from: ", fromTheme, "to:", toTheme);
	applayTheme(toTheme);
	setTheme(toTheme);
	// setEditorTheme()
}

jQuery(document).ready(($) => {
	init();
	$(".navbar-burger").click(() => {
		$(".navbar-burger").toggleClass("is-active");
		$(".navbar-menu").toggleClass("is-active");
	});

	$(".modal-button").click(function () {
		const target = $(this).data("target");
		$("html").addClass("is-clipped");
		$(target).addClass("is-active");
	});

	$(".modal-background, .modal-close").click(function () {
		$("html").removeClass("is-clipped");
		$(this).parent().removeClass("is-active");
	});

	$(".modal-card-head .delete, .modal-card-foot .button").click(() => {
		$("html").removeClass("is-clipped");
		$("#modal-ter").removeClass("is-active");
	});

	$(document).on("keyup", (e) => {
		if (e.keyCode === 27) {
			$("html").removeClass("is-clipped");
			$(".modal").removeClass("is-active");
		}
	});

	const $highlights = $(".highlight");

	$highlights.each(function () {
		const $el = $(this);
		const copy = '<button class="copy">Copy</button>';
		const expand = '<button class="expand">Expand</button>';
		$el.append(copy);

		if ($el.find("pre code").innerHeight() > 600) {
			$el.append(expand);
		}
	});

	const $highlightButtons = $(".highlight .copy, .highlight .expand");

	$highlightButtons.hover(
		function () {
			$(this).parent().css("box-shadow", "0 0 0 1px #ed6c63");
		},
		function () {
			$(this).parent().css("box-shadow", "none");
		},
	);

	$(".highlight .expand").click(function () {
		$(this).parent().children("pre").css("max-height", "none");
	});

	if ("Clipboard" in window) {
		const _cb = new Clipboard(".copy", {
			target: (trigger) => trigger.previousSibling,
		});
	}
});
