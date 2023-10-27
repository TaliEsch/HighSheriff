// These are the links in the table, which will open a new Modal
let modalLinks = document.getElementsByClassName("modal-link");

// Gets the modal (pop-up window)
let modal = document.getElementById("modal");
// The close button for the modal
let closeModal = document.getElementsByClassName("close")[0];
// The modal header, will contain applicant name
let modalHeader = document.getElementById("modal-header");
// The video element to embed into the modal
let modalVideo = document.getElementById("modal-video");
// The source used for the video to play
let videoSource = document.createElement("source");

for (let i = 0; i < modalLinks.length; i++) {
  modalLinks[i].addEventListener("click", (e) => {
    let tableRow = e.target.parentNode.parentNode;
    let firstName = tableRow.children[1].textContent;
    let surname = tableRow.children[2].textContent;
    let filename = tableRow.children[4].textContent;
    // Set text of modal header
    modalHeader.innerHTML = `${firstName} ${surname}`;
    // Sends a request to the server to find the video
    videoSource.setAttribute("src", `/display/${filename}`);
    // Gets the type of the video, e.g. "mp4" or "mov"
    videoSource.setAttribute("type", `video/${filename.match(/\.[0-9a-z]+/)[0].slice(1)}`);
    modalVideo.appendChild(videoSource);
    modal.style.display = "block";
    modalVideo.play();
  });
}

closeModal.addEventListener("click", () => {
  stopVideo(modalVideo);
  modal.style.display = "none";
});

window.addEventListener("click", (e) => {
  if (e.target == modal) {
    stopVideo(modalVideo);
    modal.style.display = "none";
  }
});

function stopVideo(videoElement) {
  videoElement.pause();
  videoElement.currentTime = 0;
}
