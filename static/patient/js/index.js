document.getElementById("toggleAppointments").addEventListener("click", function () {
    var section = document.getElementById("appointmentsSection");
    if (section.classList.contains("hidden")) {
        section.classList.remove("hidden");
        this.textContent = "Hide My Appointments";
    } else {
        section.classList.add("hidden");
        this.textContent = "View My Appointments";
    }
});