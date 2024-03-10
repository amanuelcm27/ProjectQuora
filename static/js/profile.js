// JavaScript to open and close the modal
document.getElementById("open-education-modal").onclick = function() {
    document.getElementById("education-modal").style.display = "block";
};

document.getElementById("close-education-modal").onclick = function() {
    document.getElementById("education-modal").style.display = "none";
};

window.onclick = function(event) {
    if (event.target == document.getElementById("education-modal")) {
        document.getElementById("education-modal").style.display = "none";
    }
};
