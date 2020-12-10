const darkSwitch = document.getElementById('switch');
const particlejs = document.getElementById('particles-js');
let dark = localStorage.getItem("dark");


const enableDarkMode = () => {
	document.body.classList.add("darkmode");
	localStorage.setItem("dark", "enabled");
	if(particlejs) {
		particlejs.style.backgroundColor="#181f2a";
	}
};

const disableDarkMode = () => {
	document.body.classList.remove("darkmode");
	localStorage.setItem("dark", "disabled");
	if (particlejs) {
		particlejs.style.backgroundColor="white";
	}
};

if (dark === "enabled") {
	enableDarkMode();
} else {
	darkSwitch.removeAttribute("checked");
}

darkSwitch.addEventListener("click", () => {
	dark = localStorage.getItem("dark");
	if (dark !== "enabled") {
		enableDarkMode();
	} else {
		disableDarkMode();
	}
});