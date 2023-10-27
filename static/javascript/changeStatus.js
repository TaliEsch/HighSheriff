/* Get id from list element for invite */
inviteBtn = document.querySelectorAll('.btn-invite');
inviteBtn.forEach(function(btn) {
  btn.addEventListener("click", function() {
    // Target export button clicked
    let inviteBtn = this;
    let isVideo = inviteBtn.classList.contains("btn-video");
    if (!isVideo) {
      // Get list id of parent container from button clicked.
      let listIDContainer = inviteBtn.parentNode.parentNode;
      // Save the id text.
      let listID = listIDContainer.firstElementChild.textContent;
      console.log(listID);
      // redirect to invite
      window.location.href = `/invite/${listID}`;
    } else {
      // Get list id of parent container from button clicked.
      let listIDContainer = inviteBtn.parentNode.parentNode;
      // Save the id text.
      let listID = listIDContainer.firstElementChild.textContent;
      console.log(listID);
      // redirect to invite
      window.location.href = `/invite/video/${listID}`;
    }
  });
});

/* Get id from list element for accept */
acceptBtn = document.querySelectorAll('.btn-accept');
acceptBtn.forEach(function(btn) {
  btn.addEventListener("click", function() {
    // Target export button clicked
    let acceptBtn = this;
    let isVideo = acceptBtn.classList.contains("btn-video");
    if (!isVideo) {
      // Get list id of parent container of export button clicked.
      let listIDContainer = acceptBtn.parentNode.parentNode;
      // Save the id text.
      let listID = listIDContainer.firstElementChild.textContent;
      console.log(listID);
      // redirect to accept
      window.location.href = `/accept/${listID}`;
    } else {
      // Get list id of parent container from button clicked.
      let listIDContainer = acceptBtn.parentNode.parentNode;
      // Save the id text.
      let listID = listIDContainer.firstElementChild.textContent;
      console.log(listID);
      // redirect to invite
      window.location.href = `/accept/video/${listID}`;
    }
  });
});

/* Get id from list element for decline */
declineBtn = document.querySelectorAll('.btn-decline');
declineBtn.forEach(function(btn) {
  btn.addEventListener("click", function() {
    // Target export button clicked
    let declineBtn = this;
    let isVideo = declineBtn.classList.contains("btn-video");
    if (!isVideo) {
      // Get list id of parent container of export button clicked.
      let listIDContainer = declineBtn.parentNode.parentNode;
      // Save the id text.
      let listID = listIDContainer.firstElementChild.textContent;
      console.log(listID);
      // redirect to decline
      window.location.href = `/decline/${listID}`;
    } else {
      // Get list id of parent container from button clicked.
      let listIDContainer = declineBtn.parentNode.parentNode;
      // Save the id text.
      let listID = listIDContainer.firstElementChild.textContent;
      console.log(listID);
      // redirect to invite
      window.location.href = `/decline/video/${listID}`;
    }
  });
});

/* Get id from list element for hold */
holdBtn = document.querySelectorAll('.btn-hold');
holdBtn.forEach(function(btn) {
  btn.addEventListener("click", function() {
    // Target export button clicked
    let holdBtn = this;
    let isVideo = holdBtn.classList.contains("btn-video");
    if (!isVideo) {
      // Get list id of parent container of export button clicked.
      let listIDContainer = holdBtn.parentNode.parentNode;
      // Save the id text.
      let listID = listIDContainer.firstElementChild.textContent;
      console.log(listID);
      // redirect to hold
      window.location.href = `/hold/${listID}`;
    } else {
      // Get list id of parent container from button clicked.
      let listIDContainer = holdBtn.parentNode.parentNode;
      // Save the id text.
      let listID = listIDContainer.firstElementChild.textContent;
      console.log(listID);
      // redirect to invite
      window.location.href = `/hold/video/${listID}`;
    }
  });
});

/* Get id from list element for shortlist */
shortlistBtn = document.querySelectorAll('.btn-shortlist');
shortlistBtn.forEach(function(btn) {
  btn.addEventListener("click", function() {
    // Target export button clicked
    let shortlistBtn = this;
    let isVideo = shortlistBtn.classList.contains("btn-video");
    if (!isVideo) {
      // Get list id of parent container of export button clicked.
      let listIDContainer = shortlistBtn.parentNode.parentNode;
      // Save the id text.
      let listID = listIDContainer.firstElementChild.textContent;
      console.log(listID);
      // redirect to shortlist
      window.location.href = `/shortlist/${listID}`;
    } else {
      // Get list id of parent container from button clicked.
      let listIDContainer = shortlistBtn.parentNode.parentNode;
      // Save the id text.
      let listID = listIDContainer.firstElementChild.textContent;
      console.log(listID);
      // redirect to invite
      window.location.href = `/shortlist/video/${listID}`;
    }
  });
});

/* Get id from list element for close */
closeBtn = document.querySelectorAll('.btn-close');
closeBtn.forEach(function(btn) {
  btn.addEventListener("click", function() {
    // Target export button clicked
    let closeBtn = this;
    let isVideo = closeBtn.classList.contains("btn-video");
    if (!isVideo) {
      // Get list id of parent container of export button clicked.
      let listIDContainer = closeBtn.parentNode.parentNode;
      // Save the id text.
      let listID = listIDContainer.firstElementChild.textContent;
      console.log(listID);
      // redirect to close
      window.location.href = `/close/${listID}`;
    } else {
      // Get list id of parent container from button clicked.
      let listIDContainer = closeBtn.parentNode.parentNode;
      // Save the id text.
      let listID = listIDContainer.firstElementChild.textContent;
      console.log(listID);
      // redirect to invite
      window.location.href = `/close/video/${listID}`;
    }
  });
});
