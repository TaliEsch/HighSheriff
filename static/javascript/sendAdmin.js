function sendContact() {

  let username = document.forms["add-admin-form"]["username"].value;

  let password = document.forms["add-admin-form"]["password"].value;

  // Compile all user inputs into a string
  params = `username=${username}&password=${password}`;
  sendValid(params);
  return false;
}

function sendValid(params) {
  // Create a POST request to send form data to server to be stored in database
  let xhttp = new XMLHttpRequest();
  xhttp.open("POST", '/addAdmin', true); // true is asynchronous
  xhttp.setRequestHeader("Content-type", "application/x-www-form-urlencoded");
  xhttp.onreadystatechange = function() {
    if (xhttp.readyState === 4 && xhttp.status === 200) {
      document.getElementById("confirmation").innerHTML = xhttp.responseText;
      console.log(xhttp.responseText);
      console.log("OK");
    }
  };
  xhttp.send(params);
}
