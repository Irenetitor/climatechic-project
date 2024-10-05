// some scripts

// jquery ready start
$(document).ready(function() {
	// jQuery code
    /* ///////////////////////////////////////
    THESE FOLLOWING SCRIPTS ONLY FOR BASIC USAGE, 
    For sliders, interactions and other
    */ ///////////////////////////////////////
	//////////////////////// Prevent closing from click inside dropdown
    $(document).on('click', '.dropdown-menu', function (e) {
      e.stopPropagation();
    });
	//////////////////////// Bootstrap tooltip
	if($('[data-toggle="tooltip"]').length>0) {  // check if element exists
		$('[data-toggle="tooltip"]').tooltip()
	} // end if   
}); 
// jquery end


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