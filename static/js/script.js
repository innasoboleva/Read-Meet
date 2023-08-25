document.querySelector('#signin-button').addEventListener('click', showPopup);

function showPopup(evt) {
    evt.preventDefault()

    const popup = document.querySelector('#signInOptions')
    popup.style.display = "flex";
    popup.style.justifyContent = "stretch";
}

// document.querySelector('#new-user-signup').addEventListener('click', newUser);

function newUser(evt) {
    evt.preventDefault()

    const formInputs = {
        'user_name': document.querySelector('#muser_name').value,
        'user_email': document.querySelector('#user_email').value,
        'user_password': document.querySelector('#user_password').value,
        'user_address': document.querySelector('#user_address').value,
        'user_age': document.querySelector('#user_age').value,
        'user_zipcode': document.querySelector('#user_zipcode').value
      }
      
    //   fetch('/api/new_user', {
    //     method: 'POST',
    //     body: JSON.stringify(formInputs),
    //     headers: {
    //       'Content-Type': 'application/json',
    //     },
    //   })
    //   .then((response) => response.json())
    //   .then((data) => {
    //     if (data['code'] == 'ERROR') {
    //         document.querySelector('#email-used-error').style.display=""; // displays error message
    //     } else {
    //         window.location.replace('/'); // reloads the page if new user successfully created, current page's navigation history replaced
    //     }
      
    //   });
}