// Display and hide answers
var acc = document.getElementsByClassName("accordion");
var i;

for (i = 0; i < acc.length; i++) {
    acc[i].addEventListener("click", function() {
        this.classList.toggle("active");
        var panel = this.nextElementSibling;
        if (panel.style.display === "block") {
        panel.style.display = "none";
        } else {
        panel.style.display = "block";
        }
    });
}

function showQuestion() {
    var x = document.getElementById("hiddenquestion");
    if (x.style.display === "none") {
        x.style.display = "block";
    } else {
        x.style.display = "none";
    }
}


// Active page
document.addEventListener('DOMContentLoaded', function() {
    var navLinks = document.querySelectorAll('.navbar-nav li a');
    var currentPageUrl = window.location.href;
    
    for (var i = 0; i < navLinks.length; i++) {
        navLinks[i].classList.remove('active');
        if (currentPageUrl.startsWith(navLinks[i].href)) {
            navLinks[i].parentElement.classList.add('active');
        }
    }
});
