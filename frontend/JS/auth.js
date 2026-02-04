const API_URL = "http://127.0.0.1:5000/api/auth";

/* ===== TOKEN HELPERS ===== */
function saveToken(token) {
    localStorage.setItem("token", token);
}

function getToken() {
    return localStorage.getItem("token");
}

/* ===== LOGIN ===== */
async function login(email, password) {
    const res = await fetch(`${API_URL}/login`, {
        method: "POST",
        headers: {
            "Content-Type": "application/json"
        },
        body: JSON.stringify({ email, password })
    });

    const data = await res.json();

    if (!res.ok) {
        alert(data.error || "Login failed");
        return;
    }

    saveToken(data.access_token);
    window.location.href = "dashboard.html";
}

/* ===== FETCH CURRENT USER ===== */
async function fetchMe() {
    const token = getToken();
    if (!token) return null;

    const res = await fetch(`${API_URL}/me`, {
        headers: {
            Authorization: "Bearer " + token
        }
    });

    if (!res.ok) return null;
    return await res.json();
}

/* ===== LOGOUT ===== */
function logout() {
    localStorage.removeItem("token");
    window.location.href = "login.html";
}
