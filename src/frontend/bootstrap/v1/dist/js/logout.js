

async function checkLogin(){
    // Ensure config is loaded before running the app
    const config = await loadConfig();
    base_url = config.base_url;  // Set global variable

    console.log("Base URL Loaded:", base_url);
    const welcomeMessage = document.getElementById("welcome_message");
    const logoutButton = document.getElementById("logout_button");
    welcomeMessage.textContent = "Loading...";

    userData = await testToken();
    if (userData && userData.full_name) {
                welcomeMessage.textContent = `${userData.full_name}, are you sure you want to log out?`;
                logoutButton.style.display = 'block';
            }
    else {
          welcomeMessage.innerHTML = "Your session has expired. Please <a target='_self' href='login.html'>login</a> again.";
    }
}
checkLogin().catch(err => console.error("checkLogin() failed:", err));


document.addEventListener("DOMContentLoaded", function () {
    const logoutButton = document.getElementById("logout_button");

    logoutButton.addEventListener("click", function () {
        showSpinner();

        fetch(`${base_url}/logout`, {  // Use the correct logout endpoint
            method: "POST",
            credentials: "include"  // ✅ Ensures cookies are included in the request
        })
        .then(response => {
            if (!response.ok) {
                throw new Error("Logout failed");
            }
            return response.json();
        })
        .then(data => {
            console.log("Logged out:", data.message);
            showAlert(data.message, "success");

            setTimeout(() => {
                window.location.href = "/login.html";  // ✅ Redirect to login page
            }, 1000);
        })
        .catch(error => {
            console.error("Error during logout:", error);
            showAlert("Failed to logout. Please try again.", "danger");
        })
        .finally(() => {
            hideSpinner();
        });
    });
});
