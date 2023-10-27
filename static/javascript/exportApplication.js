/* Get id from list element  */
exportBtn = document.querySelectorAll('.btn-export');
exportBtn.forEach(function(btn) {
  btn.addEventListener("click", function() {
    /* Target export button clicked  */
    var exportBtn = this;
    /* Get list id of parent container of export button clicked. */
    var listIDContainer = exportBtn.parentNode.parentNode;
    /* Save the id text. */
    var listID = listIDContainer.firstElementChild.textContent;
    console.log(listID);
    // loadExport(listID);
    window.location.href = `/export/${listID}`;
  });
});

/* AJAX Redundent  */

// function loadExport(listID){
//   params = listID;
//   var xhttp = new XMLHttpRequest();
//   xhttp.open("POST", `/export/${params}`, true); // true is asynchronous
//   xhttp.setRequestHeader("Content-type", "application/x-www-form-urlencoded");
//   xhttp.onload = function() {
//     if (xhttp.readyState === 4 && xhttp.status === 200) {
//       console.log(xhttp.responseText);
//       window.location.href = `/export/${params}`;
//     } else {
//       console.error(xhttp.statusText);
//     }
//   };
//   xhttp.send(params);
//   return true;
// }
