document.addEventListener('DOMContentLoaded', function () {
    const openAddressModal = document.getElementById('openAddressModal');
    const closeAddressModal = document.getElementById('closeAddressModal');
    const cancelAddressModal = document.getElementById('cancelAddressModal');
    const addressModal = document.getElementById('addressModal');
    const addressForm = document.getElementById('address-form');

    // Open Address Modal
    openAddressModal.addEventListener('click', function () {
        addressModal.classList.remove('hidden');
    });

    // Close Address Modal
    closeAddressModal.addEventListener('click', function () {
        addressModal.classList.add('hidden');
    });

    cancelAddressModal.addEventListener('click', function () {
        addressModal.classList.add('hidden');
    });

    // Form validation and submission
    addressForm.addEventListener('submit', function (event) {
        event.preventDefault();

        // Form Validation
        const addressLineOne = document.getElementById('address_line_one').value;
        const locality = document.getElementById('locality').value;
        const city = document.getElementById('city').value;
        const state = document.getElementById('state').value;
        const country = document.getElementById('country').value;

        if (!addressLineOne || !locality || !city || !state || !country) {
            alert('Please fill all the fields.');
            return;
        }

        // If validation is passed, submit the form
        const formData = new FormData(addressForm);
        fetch(addressForm.action, {
            method: 'POST',
            body: formData,
        })
        .then(() => {
            // Refresh the page
            window.location.reload();
        })
        .catch(error => {
            console.error('Error:', error);
            alert('An error occurred while updating the address.');
        });
    });
});