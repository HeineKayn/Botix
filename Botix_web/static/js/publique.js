function updateScroll(){
    var element = document.getElementsByClassName("messages_section")[0];
    element.scrollTop = element.scrollHeight;
}

document.addEventListener("DOMContentLoaded", function() {
  updateScroll();
});