/**
 * Checks to see if the string contains a number.
 * @param {string} string the string to be checked.
 * @param {string} error_message the error message to display
 *                               if the string contains a number.
 * @returns {boolean} true if string contains a number,
 *                    false otherwise.
*/
function hasNumber(string, error_message="Error!") {
  if (string.match(/\d+/g) != null) {
    alert(error_message);
    return true;
  }
  return false;
}

function sendApplication() {
  // Check if there is a number in first name
  let firstName = document.forms["application-form"]["firstName"].value;
  if (hasNumber(firstName, "First name cannot contain a number!")) return false;

  // Check if there is a number in surname
  let surname = document.forms["application-form"]["surname"].value;
  if (hasNumber(surname, "Surname cannot contain a number!")) return false;

  // Email should be checked by HTML validation
  let email = document.forms["application-form"]["email"].value;

  let question1 = document.forms["application-form"]["question1"].value;
  let question2 = document.forms["application-form"]["question2"].value;
  let question3 = document.forms["application-form"]["question3"].value;
  let question4 = document.forms["application-form"]["question4"].value;
  let question5 = document.forms["application-form"]["question5"].value;

  // Compile all user inputs into a string
  let params = `firstName=${firstName}&surname=${surname}&email=${email}&question1=${question1}\
&question2=${question2}&question3=${question3}&question4=${question4}&question5=${question5}`;

  let xhttp = new XMLHttpRequest();
  xhttp.open("POST", `/applications`, true); // true is asynchronous
  xhttp.setRequestHeader("Content-type", "application/x-www-form-urlencoded");
  xhttp.onreadystatechange = function() {
    if (xhttp.readyState === 4 && xhttp.status === 200) {
      console.log(xhttp.responseText);
      document.getElementById("text-accepted").innerHTML = xhttp.responseText;
    }
  };
  xhttp.send(params);
  return false;
}

function sendUpload() {
  // Check if there is a number in first name
  let firstName = document.forms["upload-form"]["uploadFirstName"].value.replace(/\s+/g,'');
  if (hasNumber(firstName, "First name cannot contain a number!")) return false;

  // Check if there is a number in surname
  let surname = document.forms["upload-form"]["uploadSurname"].value.replace(/\s+/g,'');
  if (hasNumber(surname, "Surname cannot contain a number!")) return false;

  // Email should be checked by HTML validation
  let email = document.forms["upload-form"]["uploadEmail"].value;

  // Gets file object to upload
  let file = document.forms["upload-form"]["uploadAppFile"].files[0];

  // Creating a FormData object to send information to the server
  // This FormData object automatically creates the params to send in
  // a key-value pair format, and allows files to be sent.
  let formData = new FormData();
  formData.append("uploadFirstName", firstName);
  formData.append("uploadSurname", surname);
  formData.append("uploadEmail", email);
  formData.append("uploadAppFile", file);

  let xhttp = new XMLHttpRequest();
  xhttp.open("POST", "/applications/upload", false); // false is synchronous
  xhttp.onreadystatechange = function() {
    if (xhttp.readyState === 4 && xhttp.status === 200) {
      console.log(xhttp.responseText);
      document.getElementById("upload-accepted").innerHTML = xhttp.responseText;
    }
  };
  xhttp.send(formData);
  return false;
}
