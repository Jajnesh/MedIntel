document.addEventListener('DOMContentLoaded', function () {
    const formFields = [
        { id: 'username', validator: validateRequired },
        { id: 'password', validator: validatePassword },
        { id: 'fname', validator: validateRequired },
        { id: 'lname', validator: validateRequired },
        { id: 'gender', validator: validateRequired },
        { id: 'email', validator: validateEmail },
        { id: 'mobile', validator: validatePhoneNumber },
        { id: 'year_of_registration', validator: validateYear },
        { id: 'qualification', validator: validateRequired },
        { id: 'specialization', validator: validateRequired },
        { id: 'aadhar_no', validator: validateRequired },
        { id: 'qualification_doc', validator: validateFile },
        { id: 'aadhar_doc', validator: validateFile },
        { id: 'terms', validator: validateTerms }
    ];

    // Attach focus event to each field
    formFields.forEach(field => {
        const fieldElement = document.getElementById(field.id);

        // Handle focus event to trigger validation on first unfilled field
        fieldElement.addEventListener('focus', function () {
            handleFieldFocus(this);
        });

        // For non-select elements, handle keyup event
        if (fieldElement.tagName !== 'SELECT') {
            if (fieldElement.type !== 'file') {
                fieldElement.addEventListener('keyup', function () {
                    field.validator(this); // Re-validate as user types
                });
            }
            else {
                fieldElement.addEventListener('change', function () {
                    field.validator(this);

                    const fileName = this.files[0]?.name;
                    if (fileName) {
                        const fileInfoElement = this.parentElement.querySelector('p.text-sm');
                        if (fileInfoElement) {
                            fileInfoElement.innerHTML = `Selected: <span class="font-semibold text-black">${fileName}</span>`;
                        }
                    }
                });
            }
        }
        // For select elements, handle change event
        else {
            fieldElement.addEventListener('change', function () {
                field.validator(this); // Re-validate as user selects an option
            });
        }
    });

    // Function to handle field focus event
    function handleFieldFocus(focusedField) {
        let firstUnfilledField = null;

        // Loop through all fields and check for the first unfilled one
        for (const field of formFields) {
            const fieldElement = document.getElementById(field.id);
            if (fieldElement.required && !fieldElement.value.trim()) {
                firstUnfilledField = fieldElement;
                break;
            }
        }

        // If there's an unfilled field before the focused field, show the error
        if (firstUnfilledField) {
            showError(firstUnfilledField, "This field is required.");
        }
    }

    // Handle form submit event
    form.addEventListener('submit', function (event) {
        event.preventDefault(); // Prevent default form submission

        let isValid = true;

        // Loop through all fields and validate
        formFields.forEach(field => {
            const fieldElement = document.getElementById(field.id);
            if (!fieldElement.classList.contains('border-red-500')) {
                field.validator(fieldElement);
                if (fieldElement.classList.contains('border-red-500')) {
                    isValid = false;
                }
            }
        });

        // If form is valid, submit via AJAX
        if (isValid) {
            // Create a FormData object to submit the form data (including files)
            const formData = new FormData(form);

            fetch("{% url 'signup_doctor' %}", {  // Update with your Django view URL
                method: 'POST',
                body: formData,
                headers: {
                    'X-CSRFToken': document.querySelector('[name=csrfmiddlewaretoken]').value  // CSRF token for Django security
                }
            })
            .then(response => response.json())
            .then(data => {
                if (data.success) {
                    alert('Form submitted successfully');
                    // Optionally, clear the form or redirect the user
                } else {
                    alert('Error: ' + data.error);
                }
            })
            .catch(error => {
                console.error('Error:', error);
                alert('Something went wrong. Please try again.');
            });
        } else {
            alert('Please fill in all required fields correctly.');
        }
    });

    // Helper Functions for Validation

    function validateRequired(field) {
        if (!field.value.trim()) {
            showError(field, "This field is required.");
        } else {
            clearError(field);
        }
    }

    function validatePassword(field) {
        const password = field.value.trim();
    
        if (password.length < 8) {
            showError(field, "Password must be at least 8 characters long.");
        }
        else if (!/[a-z]/.test(password)) {
            showError(field, "Password must contain at least one lowercase letter.");
        }
        else if (!/[A-Z]/.test(password)) {
            showError(field, "Password must contain at least one uppercase letter.");
        }
        else if (!/[0-9]/.test(password)) {
            showError(field, "Password must contain at least one number.");
        }
        else if (!/[!@#$%^&*(),.?":{}|<>]/.test(password)) {
            showError(field, "Password must contain at least one special character.");
        }
        else {
            clearError(field);
        }
    }
    

    function validateEmail(field) {
        const emailPattern = /^[a-zA-Z0-9._-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,6}$/;
        if (!emailPattern.test(field.value)) {
            showError(field, "Please enter a valid email address.");
        } else {
            clearError(field);
        }
    }

    function validatePhoneNumber(field) {
        const phonePattern = /^[0-9]{10}$/;
        if (!phonePattern.test(field.value)) {
            showError(field, "Please enter a valid phone number (10 digits).");
        } else {
            clearError(field);
        }
    }

    function validateYear(field) {
        const yearValue = parseInt(field.value);
        if (yearValue < 1900 || yearValue > 2025) {
            showError(field, "Please enter a year between 1900 and 2025.");
        } else {
            clearError(field);
        }
    }

    function validateFile(field) {
        const validFileTypes = ['application/pdf'];
        clearError(field);
        if (field.files.length > 0) {
            const file = field.files[0];
            if (file.size > 1 * 1024 * 1024) {
                showError(field, "File must be less than 1MB.");
            } else if (!validFileTypes.includes(file.type)) {
                showError(field, "File must be PDF.")
            } else {
                clearError(field);
            }
        }
    }

    function validateTerms(field) {
        if (!field.checked) {
            showError(field, "You must agree to the Terms and Conditions.");
        } else {
            clearError(field);
        }
    }

    function showError(field, message) {
        let errorElement = document.getElementById(field.id + "_error");
        if (!errorElement) {
            errorElement = document.createElement('p');
            errorElement.classList.add('error-message', 'text-red-500', 'text-sm');
            field.parentNode.insertBefore(errorElement, field.nextSibling);
        }
        errorElement.textContent = message;
        field.classList.add('border-red-500');
    }

    function clearError(field) {
        let errorElement = document.getElementById(field.id + "_error");
        if (errorElement && errorElement.classList.contains('error-message')) {
            errorElement.textContent = '';
        }
        field.classList.remove('border-red-500');
    }
});
