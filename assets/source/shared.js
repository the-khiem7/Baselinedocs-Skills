// Theme switch for the README illustrations: ?theme=dark selects the dark tokens in shared.css.
document.documentElement.dataset.theme = new URLSearchParams(location.search).get("theme") === "dark" ? "dark" : "light";
