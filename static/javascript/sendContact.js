function sendContact() {

  let name = document.forms["contact-form"]["name"].value;
  // Check if there is a number in name
  if (name.match(/\d+/g) != null) {
    alert('name cannot contain a number!');
    return false;
  }

  let email = document.forms["contact-form"]["email"].value;

  let message = document.forms["contact-form"]["message"].value;

  // Compile all user inputs into a string
  params = `name=${name}&email=${email}&message=${message}`;
  sendValid(params);
  return false;
}

function sendValid(params) {
  // Create a POST request to send form data to server to be stored in database
  let xhttp = new XMLHttpRequest();
  xhttp.open("POST", '/contact', true); // true is asynchronous
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
