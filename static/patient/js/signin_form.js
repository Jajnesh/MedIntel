document.addEventListener('DOMContentLoaded', function () {
    const formFields = [
        { id: 'username', validator: validateRequired },
        { id: 'password', validator: validateRequired }
    ];

    // Attach focus event to each field
    formFields.forEach(field => {
        const fieldElement = document.getElementById(field.id);

        // Handle focus event to trigger validation on first unfilled field
        fieldElement.addEventListener('focus', function () {
            handleFieldFocus(this);
        });

        // Handle keyup event
        fieldElement.addEventListener('keyup', function () {
            field.validator(this); // Re-validate as user types
        });
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

            fetch("{% url 'signin_patient' %}", {  // Update with your Django view URL
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
