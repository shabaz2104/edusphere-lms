document.addEventListener("DOMContentLoaded", () => {

    const body = document.body;
    const toggleBtn = document.getElementById("themeToggle");

    /* =========================
       APPLY SAVED THEME FIRST
    ========================= */
    const savedTheme = localStorage.getItem("theme");
    if (savedTheme === "dark") {
        body.classList.add("dark");
    }

    if (toggleBtn) {
        toggleBtn.textContent = body.classList.contains("dark") ? "☀️" : "🌙";

        toggleBtn.addEventListener("click", () => {
            body.classList.toggle("dark");

            const isDark = body.classList.contains("dark");
            toggleBtn.textContent = isDark ? "☀️" : "🌙";
            localStorage.setItem("theme", isDark ? "dark" : "light");
        });
    }

    /* =========================
       MOBILE MENU
    ========================= */
    const menuToggle = document.querySelector(".menu-toggle");
    const navLinks = document.querySelector(".nav-links");

    if (menuToggle && navLinks) {
        menuToggle.addEventListener("click", () => {
            navLinks.classList.toggle("active");
        });
    }

    /* =========================
       CONTACT FORM
    ========================= */
    const form = document.getElementById("contactForm");
    if (form) {
        form.addEventListener("submit", (e) => {
            e.preventDefault();

            const name = document.getElementById("name").value.trim();
            const email = document.getElementById("email").value.trim();
            const message = document.getElementById("message").value.trim();

            if (!name || !email || !message) {
                alert("Please fill in all fields.");
                return;
            }

            alert("Message sent successfully! (Demo)");
            form.reset();
        });
    }
});


