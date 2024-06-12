const form = document.getElementById("form");

if (form) {
    form.addEventListener("submit", (e) => {
        e.preventDefault();
        const username = document.getElementById("username").value;
        const password = document.getElementById("password").value;
        const number = document.getElementById("number").value;
        if (validateForm(username, password, number)) {
            register(username, password, number);
        }
    });
}

function validateForm(username, password, number) {
    if (username.trim() === "" || password.trim() === "" || number.trim() === "") {
        alert("Please fill in all fields.");
        return false;
    }
    return true;
}

function register(username, password, number) {
    const user = {
        "username": username,
        "password": password,
        "number": number
    };

    let users = JSON.parse(localStorage.getItem('users')) || {};

    if (users.hasOwnProperty(username)) {
        alert("You are already registered.");
    } else {
        users[username] = user;
        localStorage.setItem('users', JSON.stringify(users));
        alert("Registration successful! You can now log in.");
        window.location.href = "/login.html";
    }
}
