const darkSwitch = document.getElementById('switch');
let dark = localStorage.getItem("dark");


const enableDarkMode = () => {
	// document.body.classList.add("darkmode");
	localStorage.setItem("dark", "enabled");
};

const disableDarkMode = () => {
	// document.body.classList.remove("darkmode");
	localStorage.setItem("dark", "disabled");
};

if (dark === "enabled") {
	enableDarkMode();
}

darkSwitch.addEventListener("click", () => {
	dark = localStorage.getItem("dark");
	if (dark !== "enabled") {
		enableDarkMode();
	} else {
		disableDarkMode();
	}
});