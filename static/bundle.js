var tuxActiveElements = document.querySelectorAll("[tux-active]");
for (let i = 0;i < tuxActiveElements.length; i++) {
  let currentElement = tuxActiveElements[i];
  let attr = currentElement.getAttribute("tux-active")?.split(" ");
  if (attr) {
    let path = attr[0];
    let classNames = attr.splice(1, attr.length);
    if (window.location.pathname == path) {
      classNames.forEach((className) => {
        currentElement.classList.add(className);
      });
    }
  }
}