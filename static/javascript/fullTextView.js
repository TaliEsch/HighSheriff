const applicationFullText = document.querySelectorAll(".fulltext");

applicationFullText.forEach(a => a.addEventListener("click", viewFullText));

function viewFullText(a) {
  const row = a.composedPath()["0"].parentNode
  const cells = row.cells
  for (let cell of cells) {
    cell.classList.toggle("fulltextView");
  }
}
