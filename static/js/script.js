// toggling buttons for sign in and sign out
const signinLink = document.getElementById("sign-in-nav-link");
const signoutLink = document.getElementById("sign-out-nav-link");

// function userIsLoggedIn() {
//     document.getElementById("user-signout").innerText = "Sign out"
//     console.log("User is logged IN")
//     signinLink.style.display = "none";
//     signoutLink.style.display = "block";
// }

// function userIsLoggedOut() {
//     document.getElementById("user-signin-nav").innerText = "Sign in"
//     console.log("User is logged OUT")
//     signinLink.style.display = "block";
//     signoutLink.style.display = "none";
// }
window.userIsLoggedIn = function () {
    document.getElementById("user-signout").innerText = "Sign out"
    console.log("User is logged IN")
    signinLink.style.display = "none";
    signoutLink.style.display = "block";
}

window.userIsLoggedOut = function () {
    document.getElementById("user-signin-nav").innerText = "Sign in"
    console.log("User is logged OUT")
    signinLink.style.display = "block";
    signoutLink.style.display = "none";
}

function closeModalWithId(modalId) {
    var modalElement = document.querySelector(`#${modalId}`);
    var modal = bootstrap.Modal.getInstance(modalElement);
    if (modal) {
        modal.hide(); // Bootstrap's method
    }
}


document.querySelector("#user-signup").addEventListener("click", (evt) => {
    evt.preventDefault();

    const formInputs = {
        user_name: document.querySelector('#user_name').value,
        user_email: document.querySelector('#user_email').value,
        user_password: document.querySelector('#user_password').value,
        user_address: document.querySelector('#user_address').value,
        user_zipcode: document.querySelector('#user_zipcode').value,
        user_age: document.querySelector('#user_age').value,
      };
    const correct_form = isFormValid(formInputs)

    console.log(correct_form)

    if (correct_form.status == "success") {
        console.log("Sending request to server to create new user...")
        fetch("/api/create_new_user", {
            method: "POST",
            body: JSON.stringify(formInputs),
            headers: { "Content-Type": "application/json" },
        })
            .then((response) => response.json())
            .then((data) => {
                if (data["status"] == "error") {
                    console.log(`${data['message']}`)
                    document.querySelector('#error-message-signup').innerText = data['message']; // displays error message
                } else {
                    userIsLoggedIn();
                    closeModalWithId("singUpForm"); // no reloading the page, only tables
                    window.updateUser(data.new_user);
                    window.updateUserOnDetailsPage(data.new_user);
                }
        });
    } else {
        document.querySelector('#error-message-signup').innerText = correct_form['message']; // displays error message
    }
});

function isFormValid(formInputs) {
    // let re = /^[\w\.-]+@[\w\.-]+\.\w+$/;
    let re = /^[\w\.-]+@[\w\.-]+\.\w+$/;
    console.log("Email check...")
    if (!(re.test(formInputs.user_email))) {
        return { "status": "error", "message": "Wrong input for email" }
    }
    
    console.log("Password check...")
    if (formInputs.user_password.length < 10) {
        return { "status": "error", "message": "Password is too short" }
    }
    if (formInputs.user_address == "") {
        return { "status": "error", "message": "Please put your address" }
    }

    re = /^\d+$/;

    console.log("Zipcode check...")
    if (!(re.test(formInputs.user_zipcode))) {
        return { "status": "error", "message": "Wrong input for Zipcode" }
    }
    console.log("Age check...")
    if (!(re.test(formInputs.user_age))) {
        return { "status": "error", "message": "User's age should be a number" }
    }
    
    return { "status": "success" }
}

document.querySelector("#user-signin").addEventListener("click", (evt) => {
    evt.preventDefault();

    const form = document.getElementById("sign-in-form");
    const formInputs = {
        user_email: document.querySelector('#email').value,
        user_password: document.querySelector('#password').value,
      };

    fetch("/api/login_user", {
        method: "POST",
        body: JSON.stringify(formInputs),
        headers: { "Content-Type": "application/json" },
    })
        .then((response) => response.json())
        .then((data) => {
            if (data["status"] == "error") {
                console.log(`${data['message']}`)
                document.querySelector('#error-message-signin').innerText = data['message']; // displays error message
            } else {
                userIsLoggedIn();
                closeModalWithId("signInWithEmail");
                window.updateUser(data.user);   // no reloading the page, only tables
                window.updateUserOnDetailsPage(data.user);
            }
    });
});


document.querySelector("#user-signout").addEventListener("click", (evt) => {
    evt.preventDefault();

    fetch("/api/logout_user")
        .then((response) => response.json())
        .then((data) => {
            if (data["status"] == "error") {
                console.log(`${data['message']}`)
                document.querySelector('#error-message-signin').innerText = data['message']; // displays error message
            } else {
                userIsLoggedOut();
                window.updateUser({"user_id": "", "name": "", "address": "", "zipcode": "" });
                window.updateUserOnDetailsPage({"user_id": "", "name": "", "address": "", "zipcode": "" });
            }
    });
});