var url = "";
var setserv = false;
function setDOMInfo(info) {
  if (!info) return;
  console.log(info);
  document.getElementById("mem").textContent = info.mus;
  url = info.url;
}
window.addEventListener("DOMContentLoaded", () => {
  // ...query for the active tab...
  chrome.tabs.query(
    {
      active: true,
      currentWindow: true,
    },
    (tabs) => {
      chrome.tabs.sendMessage(
        tabs[0].id,
        { from: "popup", subject: "DOMInfo" },
        // ...also specifying a callback to be called
        //    from the receiving end (content script).
        setDOMInfo
      );
    }
  );
});
document
  .getElementById("settingsBU")
  .addEventListener("click", changeServer_State);
function changeServer_State() {
  let settiings = document.getElementById("chanSer");
  console.log(settiings.style.display, setserv);
  setserv = !setserv;
}
function changeServer() {}
