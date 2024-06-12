const form = document.getElementById("form");

if (form) {
    form.addEventListener("submit", (e) => {
        e.preventDefault();
        const username = document.getElementById("username").value;
        const password = document.getElementById("password").value;
        if (validateForm(username, password)) {
            login(username, password);
        }
    });
}

function validateForm(username, password) {
    if (username.trim() === "" || password.trim() === "") {
        alert("Please enter both username and password.");
        return false;
    }
    return true;
}

function login(username, password) {
    const users = JSON.parse(localStorage.getItem('users')) || {};

    if (users.hasOwnProperty(username) && users[username].password === password) {
        alert("Login successful! Redirecting to index.html");
        window.location.href = "/index.html";
    } else {
        alert("Invalid username or password. Please try again or sign up.");
    }
}


