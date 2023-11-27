// This event listener ensures that the code runs after the DOM has loaded.


document.addEventListener("DOMContentLoaded", function() {

   // Select all elements with the class 'content-animated' and blur classes
    const contents = document.getElementsByClassName("content-animated");
    const blurElements = document.querySelectorAll('.blur, .blue-blur');

    // Function to add 'fade-in' class and toggle blur
    function addAnimations() {
    for (let content of contents) {
        content.classList.add("fade-in"); // Add the CSS class for fade-in animation
    }

    blurElements.forEach(el => el.classList.add('active')); // Activate blur effect
    }

    // Call the function to apply changes
    addAnimations();


});


    const text = `
        Welcome to Spotify Stats!
        `;
    const speed = 100; // Time in milliseconds
    let i = 0;

    function typeText() {
        if (i < text.length) {
            document.getElementById("dynamic-text").textContent += text.charAt(i);
            i++;
            setTimeout(typeText, speed);
        }
    }

    // Start the animation when the page is loaded
    document.addEventListener('DOMContentLoaded', typeText);







