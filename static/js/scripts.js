document.addEventListener("DOMContentLoaded", function () {
    const yearSelect = document.getElementById("year");
    const monthSelect = document.getElementById("month");
    const daySelect = document.getElementById("day");

    function updateDays() {
        const year = parseInt(yearSelect.value);
        const month = parseInt(monthSelect.value);

        daySelect.innerHTML = "";

        const defaultOption = document.createElement("option");
        defaultOption.value = "";
        defaultOption.text = "Day";
        daySelect.appendChild(defaultOption);

        if (!year || !month) return; 

        const daysInMonth = new Date(year, month, 0).getDate();

        for (let d = 1; d <= daysInMonth; d++) {
            const option = document.createElement("option");
            option.value = d;
            option.text = d;
            daySelect.appendChild(option);
        }
    }

    yearSelect.addEventListener("change", updateDays);
    monthSelect.addEventListener("change", updateDays);
});

document.getElementById("show_password").addEventListener("click", function() {
    const password_field = document.getElementById("password");
    if (password_field.type === "password"){
        password_field.type = "text";
    } else {
        password_field.type = "password";
    }
});

document.getElementById("show_password").addEventListener("click", function() {
    const password_field1 = document.getElementById("password1");
    const password_field2 = document.getElementById("password2");
    const password_field3 = document.getElementById("old_password");
    if (password_field1.type === "password" && password_field2.type === "password"){
        password_field1.type = "text";
        password_field2.type = "text";
        password_field3.type = "text";
    } else {
        password_field1.type = "password";
        password_field2.type = "password";
        password_field3.type = "password";
    }
});

