
function togglePassword() {
    const eyeIcon = document.querySelector('.eye-icon');
    const passwordInput = document.getElementById('password');
    if (passwordInput.type == "password") {
        passwordInput.type = "text";
        eyeIcon.src = "static/img/visible.png";
    } else {
        passwordInput.type = "password";
        eyeIcon.src = "static/img/hide.png";
    }
}

const rForm = document.getElementById("r-form");
if (rForm !== null) {
    rForm.addEventListener("submit", function(e) {

        let name = document.getElementById("name").value;
        let email = document.getElementById("email").value;
        let password = document.getElementById("password").value;
        const err = document.querySelector(".registration-login-form-error");
        const emailPattern = /^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$/;
        const passwordPattern = /^[A-Za-z0-9!@#$%^&*()\-_+=.,<>/?\[\]{}\\|`~]+$/;

        if (name.length < 4) {
            e.preventDefault();
            err.textContent = "Мінімальна довжина імені - 4 символи !";
        } else if (email.length < 4) {
            e.preventDefault();
            err.textContent = "Мінімальна довжина пошти - 4 символи !";
        }  else if (password.length < 4) {
            e.preventDefault();
            err.textContent = "Мінімальна довжина паролю - 4 символи !";
        } else if (!emailPattern.test(email)) {
            e.preventDefault();
            err.textContent = "Невірний формат пошти !";
        } else if (!passwordPattern.test(password)) {
            e.preventDefault();
            err.textContent = "Пароль може складатись тільки з латинських малих та великих літер, цифр та символів !@#$%^&*()-_=+.,<>/?[]{}\\|~";
        }

    });
}

const lForm = document.getElementById("l-form");
if (lForm !== null) {
    lForm.addEventListener("submit", function(e) {

        let email = document.getElementById("email").value;
        let password = document.getElementById("password").value;
        const err = document.querySelector(".registration-login-form-error");
        const emailPattern = /^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$/;
        const passwordPattern = /^[A-Za-z0-9!@#$%^&*()\-_+=.,<>/?\[\]{}\\|`~]+$/;

        if (email.length < 4) {
            e.preventDefault();
            err.textContent = "Мінімальна довжина пошти - 4 символи !";
        }  else if (password.length < 4) {
            e.preventDefault();
            err.textContent = "Мінімальна довжина паролю - 4 символи !";
        } else if (!emailPattern.test(email)) {
            e.preventDefault();
            err.textContent = "Невірний формат пошти !";
        } else if (!passwordPattern.test(password)) {
            e.preventDefault();
            err.textContent = "Пароль може складатись тільки з латинських малих та великих літер, цифр та символів !@#$%^&*()-_=+.,<>/?[]{}\\|~";
        }

    });
}

const addForm = document.getElementById("add-form");
if (addForm !== null) {
    addForm.addEventListener("submit", function(e) {

        let number = document.getElementById("meter-num").value;
        const err = document.querySelector(".add-form-error");
        const numPattern = /^\d+$/;

        if (number.length == 0) {
            e.preventDefault();
            err.textContent = "Номер повинен містити принаймні одну цифру";
        } else if (number.length > 12) {
            e.preventDefault();
            err.textContent = "Максимальна довжина номеру - 12 символів !";
        } else if (!numPattern.test(number)) {
            e.preventDefault();
            err.textContent = "Номер повинен містити тільки цифри";
        }

    });
}

const sendForm = document.getElementById("send-form");
if (sendForm !== null) {
    sendForm.addEventListener("submit", function(e) {

        let meterValue = document.getElementById('choice-field').value;
        let dayValue = document.getElementById("day-value").value;
        let nightValue = document.getElementById("night-value").value;
        const err = document.querySelector(".send-form-error");
        const numPattern = /^\d+$/;

        if (meterValue === "") {
            e.preventDefault();
            err.textContent = "Ви не вибрали лічильник (якщо у список пустий, то спочатку вам потрібно додати його) !";
        } else if (dayValue.length == 0) {
            e.preventDefault();
            err.textContent = "Введіть значення денного показника";
        } else if (nightValue.length == 0) {
            e.preventDefault();
            err.textContent = "Введіть значення нічного показника";
        } else if (!numPattern.test(dayValue)) {
            e.preventDefault();
            err.textContent = "Значення денного показника має містити тільки цифри";
        } else if (!numPattern.test(nightValue)) {
            e.preventDefault();
            err.textContent = "Значення нічного показника має містити тільки цифри";
        } else if (dayValue.length > 10) {
            e.preventDefault();
            err.textContent = "Значення денного показника занадто велике";
         } else if (nightValue.length > 10) {
            e.preventDefault();
            err.textContent = "Значення нічного показника занадто велике";
        }

    });
}



