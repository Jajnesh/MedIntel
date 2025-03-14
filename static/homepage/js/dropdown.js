document.addEventListener("DOMContentLoaded", function () {
    const dropdownButtons = document.querySelectorAll("[data-dropdown-toggle]");

    dropdownButtons.forEach((button) => {
        const dropdownMenu = button.nextElementSibling;

        if (dropdownMenu) {
            let timeoutId;

            button.addEventListener("mouseenter", function () {
                clearTimeout(timeoutId);
                dropdownMenu.classList.remove("hidden");
            });
            button.addEventListener("mouseleave", function () {
                timeoutId = setTimeout(() => {
                    if (!dropdownMenu.matches(":hover")) {
                        dropdownMenu.classList.add("hidden");
                    }
                },50);
            });
            dropdownMenu.addEventListener("mouseenter", function () {
                clearTimeout(timeoutId);
                dropdownMenu.classList.remove("hidden");
            });
            dropdownMenu.addEventListener("mouseleave", function () {
                timeoutId = setTimeout(() => {
                    dropdownMenu.classList.add("hidden");
                },0);
            });
        }
    });
});
