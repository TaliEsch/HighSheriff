function loginValidation() {
    // Username validation for registration form
    let username = document.forms["registrationForm"]["username"].value;
    if (username === "") {
        alert("The username field cannot be left blank");
        return false;
    }
    if (username.length >= 32 ) {
        alert("Entered username is too long")
        return false;
    }
    // Password validation for registration form, ensures password is between 8 and 32 characters and not left empty
    let password = document.forms["registrationForm"]["password"].value;
    if (password === "") {
        alert("The password field cannot be left blank");
        return false;
    }
    if (password.length >= 32) {
        alert("Entered password is too long")
        return false;
    }
    if (password.length <= 8){
        alert("Entered password is too short, please make it above 8 characters")
        return false;
    }
}