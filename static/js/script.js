function closeModalWithId(modalId) {
    var modalElement = document.querySelector(`#${modalId}`);
    var modal = bootstrap.Modal.getInstance(modalElement);
    if (modal) {
        modal.hide(); // Bootstrap's method
    }
}

document.querySelector("#user-signup").addEventListener("click", (evt) => {
    evt.preventDefault();

    const form = document.getElementById("sign-up-form");
    const formInputs = {
        user_name: document.querySelector('#user_name').value,
        user_email: document.querySelector('#user_email').value,
        user_password: document.querySelector('#user_password').value,
        user_address: document.querySelector('#user_address').value,
        user_zipcode: document.querySelector('#user_zipcode').value,
        user_age: document.querySelector('#user_age').value,
      };

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
                // closeModalWithId("singUpForm");
                window.location.replace("/"); // reloads the page if new user successfully created, current page's navigation history replaced
            }
    });
});