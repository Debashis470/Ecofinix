// Glassmorphism Login Form – Clean & Stable JS

document.addEventListener("DOMContentLoaded", () => {

    const form = document.getElementById("loginForm");
    const successMessage = document.getElementById("successMessage");
    const submitBtn = document.querySelector(".login-btn");
    const inputs = document.querySelectorAll(".input-wrapper input");
    const passwordInput = document.getElementById("password");
    const passwordToggle = document.getElementById("passwordToggle");

    /* ---------------- FLOATING LABELS ---------------- */
    inputs.forEach(input => {
        const wrapper = input.parentElement;

        // on load / autofill
        if (input.value.trim() !== "") {
            wrapper.classList.add("filled");
        }

        input.addEventListener("focus", () => {
            wrapper.classList.add("focused");
        });

        input.addEventListener("blur", () => {
            wrapper.classList.remove("focused");
            input.value.trim() !== ""
                ? wrapper.classList.add("filled")
                : wrapper.classList.remove("filled");
        });

        input.addEventListener("input", () => {
            input.value.trim() !== ""
                ? wrapper.classList.add("filled")
                : wrapper.classList.remove("filled");
        });
    });

    /* ---------------- PASSWORD TOGGLE ---------------- */
    if (passwordToggle && passwordInput) {
        passwordToggle.addEventListener("click", () => {
            const eye = passwordToggle.querySelector(".eye-icon");
            const isPassword = passwordInput.type === "password";

            passwordInput.type = isPassword ? "text" : "password";
            eye.classList.toggle("show-password", isPassword);
        });
    }

    /* ---------------- FORM SUBMIT ---------------- */
    form.addEventListener("submit", e => {
        e.preventDefault();

        const email = document.getElementById("email").value.trim();
        const password = passwordInput.value.trim();

        let valid = true;

        if (!email || !email.includes("@")) {
            showError("email", "Enter a valid email");
            valid = false;
        } else clearError("email");

        if (password.length < 6) {
            showError("password", "Minimum 6 characters");
            valid = false;
        } else clearError("password");

        if (!valid) {
            shake(form);
            return;
        }

        // loading state
        submitBtn.classList.add("loading");

        // simulate login
        setTimeout(() => {
            submitBtn.classList.remove("loading");
            form.style.display = "none";
            successMessage.classList.add("show");
        }, 1200);
    });

    /* ---------------- HELPERS ---------------- */
    function showError(id, msg) {
        const error = document.getElementById(id + "Error");
        if (error) error.innerText = msg;
    }

    function clearError(id) {
        const error = document.getElementById(id + "Error");
        if (error) error.innerText = "";
    }

    function shake(el) {
        el.style.animation = "shake 0.4s";
        setTimeout(() => el.style.animation = "", 400);
    }
});

/* ---------------- PAGE VISIBILITY UX ---------------- */
document.addEventListener("visibilitychange", () => {
    if (document.visibilityState === "visible") {
        const emailInput = document.getElementById("email");
        if (emailInput && !emailInput.value) {
            setTimeout(() => emailInput.focus(), 100);
        }
    }
});
