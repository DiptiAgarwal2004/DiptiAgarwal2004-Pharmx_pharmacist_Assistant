function showHero() {
    document.getElementById("hero").style.display = "flex"; // Show Hero
    document.getElementById("loginPage").style.display = "none"; // Hide Login
    document.getElementById("signupPage").style.display = "none"; // Hide Signup
}

function showLogin() {
    document.getElementById("hero").style.display = "none"; // Hide Hero
    document.getElementById("loginPage").style.display = "flex"; // Show Login
    document.getElementById("signupPage").style.display = "none"; // Hide Signup
}

function showSignup() {
    document.getElementById("hero").style.display = "none"; // Hide Hero
    document.getElementById("signupPage").style.display = "flex"; // Show Signup
    document.getElementById("loginPage").style.display = "none"; // Hide Login
}
