const authBtn = document.getElementById("auth-btn");
const cookieBtn = document.getElementById("cookie-btn");
const cookieInfo = document.getElementById("cookie-info");
const securitySettings = document.getElementById("security-settings");
const authStatus = document.getElementById("auth-status");
const authStatusIndicator = document.getElementById("auth-status-indicator");
const sensitiveInfo = document.getElementById("sensitive-info");
const secretKey = document.getElementById("secret-key");

/*authBtn.addEventListener("click", async () => {
    const secureFlag = document.getElementById("secure-flag").checked;
    const httponlyFlag = document.getElementById("httponly-flag").checked;
    const samesiteFlag = document.getElementById("samesite-flag").value;

    const response = await fetch("/auth", {
        method: "POST",
        headers: {
            'Content-Type': 'application/x-www-form-urlencoded'
        },
        body: `secure=${secureFlag}&httponly=${httponlyFlag}&samesite=${samesiteFlag}`,
        credentials: "include"
    });
    const data = await response.json();
    if (data.success) {
        authStatusIndicator.style.backgroundColor = "green";
        sensitiveInfo.style.display = "block";
        secretKey.innerText = "1234567890";
    }
});*/

cookieBtn.addEventListener("click", async () => {
    cookieInfo.innerText = `Cookie: ${document.cookie}`;
});