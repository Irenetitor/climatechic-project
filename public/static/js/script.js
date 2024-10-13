// some scripts
window.onload = function () {
    console.log("website is loaded!!");
    const hamburger = document.querySelector(".hamburger");

    // Enable/Disable mobile nav menu
    hamburger.addEventListener("click", function () {
        console.log("clicked");
        hamburger.classList.toggle("is-active");
        slideToggle(document.querySelector('.menu-mobile'));
    });

    function slideToggle(element, duration = 400) {
        if (window.getComputedStyle(element).display === 'none') {
            return slideDown(element, duration);
        } else {
            return slideUp(element, duration);
        }
    }
    
    function slideUp(element, duration = 400) {
        element.style.transitionProperty = 'height, margin, padding';
        element.style.transitionDuration = duration + 'ms';
        element.style.boxSizing = 'border-box';
        element.style.height = element.offsetHeight + 'px';
        element.offsetHeight; // Force repaint
    
        element.style.overflow = 'hidden';
        element.style.height = 0;
        element.style.paddingTop = 0;
        element.style.paddingBottom = 0;
        element.style.marginTop = 0;
        element.style.marginBottom = 0;
    
        window.setTimeout(() => {
            element.style.display = 'none';
            element.style.removeProperty('height');
            element.style.removeProperty('padding-top');
            element.style.removeProperty('padding-bottom');
            element.style.removeProperty('margin-top');
            element.style.removeProperty('margin-bottom');
            element.style.removeProperty('overflow');
            element.style.removeProperty('transition-duration');
            element.style.removeProperty('transition-property');
        }, duration);
    }
    
    function slideDown(element, duration = 400) {
        element.style.removeProperty('display');
        let display = window.getComputedStyle(element).display;

        if (display === 'none') {
            display = 'block';
        }

        element.style.display = display;
        let height = element.offsetHeight;
        element.style.overflow = 'hidden';
        element.style.height = 0;
        element.style.paddingTop = 0;
        element.style.paddingBottom = 0;
        element.style.marginTop = 0;
        element.style.marginBottom = 0;
        element.offsetHeight; // Force repaint
        element.style.boxSizing = 'border-box';
        element.style.transitionProperty = 'height, margin, padding';
        element.style.transitionDuration = duration + 'ms';
        element.style.height = height + 'px';
        element.style.removeProperty('padding-top');
        element.style.removeProperty('padding-bottom');
        element.style.removeProperty('margin-top');
        element.style.removeProperty('margin-bottom');

        window.setTimeout(() => {
            element.style.removeProperty('height');
            element.style.removeProperty('overflow');
            element.style.removeProperty('transition-duration');
            element.style.removeProperty('transition-property');
        }, duration);
    }

}

function validateRegisterForm() {
    const firstNameDOM = document.getElementById('first-name');
    const lastNameDOM = document.getElementById('last-name');
    const emailDOM = document.getElementById('email');
    const passwordDOM = document.getElementById('password');
    const statusMessageDOM = document.getElementById('status-message');
  
    // Validate first name
    const namePattern = /^[A-Za-z\s]+$/;
    let firstName = firstNameDOM.value;
    if (firstName.trim() === "") {
        statusMessageDOM.textContent = "First Name is empty. Please enter your first name!";
        statusMessageDOM.style.display = "block";
        return false;
    } else if (!namePattern.test(firstName)) {
        statusMessageDOM.textContent = "Please enter a valid first name (letters only)!";
        statusMessageDOM.style.display = "block";
        return false;
    }
  
    // Validate last name
    let lastName = lastNameDOM.value;
    if (lastName.trim() === "") {
        statusMessageDOM.textContent = "Last Name is empty. Please enter your last name!";
        statusMessageDOM.style.display = "block";
        return false;
    } else if (!namePattern.test(lastName)) {
        statusMessageDOM.textContent = "Please enter a valid last name (letters only)!";
        statusMessageDOM.style.display = "block";
        return false;
    }
  
    // Validate email
    const emailPattern = /^[^\s@]+@[^\s@]+\.[^\s@]+$/;
    let email = emailDOM.value;
    if (email.trim() === "") {
        statusMessageDOM.textContent = "Email is empty. Please enter your email!";
        statusMessageDOM.style.display = "block";
        return false;
    } else if (!emailPattern.test(email)) {
        statusMessageDOM.textContent = "Please enter a valid email address!";
        statusMessageDOM.style.display = "block";
        return false;
    }
  
    // Validate password
    let password = passwordDOM.value;
    if (password.trim() === "") {
        statusMessageDOM.textContent = "Password is empty. Please enter your password!";
        statusMessageDOM.style.display = "block";
        return false;
    }
  
    // Hide the status message if validation passes
    statusMessageDOM.style.display = "none";
    return true;
  }