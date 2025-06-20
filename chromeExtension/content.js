chrome.runtime.onMessage.addListener((msg, sender, response) => {
  if (msg.from === "popup" && msg.subject === "DOMInfo") {
    let atag = document.getElementsByClassName("d-link deco-link track__title");
    let nnn = document.getElementsByClassName(
      "d-artists d-artists__expanded"
    )[0].firstChild;
    var domInfo = {
      mus: `${atag[0].innerHTML} - ${nnn.innerHTML}`,
      url: atag[0].href,
    };
    response(domInfo);
  }
});
