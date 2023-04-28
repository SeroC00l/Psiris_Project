document.addEventListener("contextmenu", function(event){
    event.preventDefault();
});

setTimeout(function () {
  var errorMessage = document.getElementById("error-message");
  if (errorMessage) {
    errorMessage.style.display = "none";
  }
}, 10000);

var lists = document.querySelectorAll(".list-group-item");
var listContextMenu = new bootstrap.Modal(
  document.getElementById("listContextMenu")
);

lists.forEach(function (list) {
  list.addEventListener("contextmenu", function (event) {
    event.preventDefault();
    listContextMenu.show(event.pageX, event.pageY);
  });
});

