async function checkLogin(){
    const welcomeMessage = document.getElementById("welcome_message");
    const loginButton = document.getElementById("login_button");

    let userData = await testToken();
    if (userData && userData.full_name) {
                welcomeMessage.innerHTML = `Welcome, ${userData.full_name}! `;
                const logoutMessage = document.createElement("p");
                logoutMessage.innerHTML = `You are logged in already. If you want to <a href="logout.html">logout</a>, click here.`;
                welcomeMessage.after(logoutMessage);
                loginButton.classList.add("disabled");
            }
    else {
          //welcomeMessage.innerHTML = "Your session has expired. Please <a target='_blank' href='login.html'>login</a> again.";
    }
}
checkLogin().catch(err => console.error("checkLogin() failed:", err));


document.addEventListener('DOMContentLoaded', async function () {
    //await initApp();  // Ensure base_url is loaded before running anything
    console.log("loginForm.addEventListener window.base_url:", window.base_url);
    const loginForm = document.getElementById('loginForm');
    loginForm.addEventListener('submit', function (e) {
        e.preventDefault();  // Prevent default form submission

        const email = document.getElementById('exampleInputEmail1').value;
        const password = document.getElementById('exampleInputPassword1').value;

        console.log("Logging in with:", email);

        showSpinner();

        fetch(`${window.base_url}/login/access-token`, {
            method: "POST",
            headers: {
                "Content-Type": "application/x-www-form-urlencoded"
            },
            body: new URLSearchParams({
                username: email,
                password: password
            }),
            credentials: "include"  // e
            // Ensures cookies (access & refresh tokens) are set
        })
        .then(response => {
            if (!response.ok) {
                throw new Error("Login failed");
            }
            return response.json();
        })
        .then(data => {
            console.log("Login successful", data);
            showAlert("Login successful!", "success");
            setTimeout(() => {
                //window.location.href = "/dashboard";  // redirect after successful login
            }, 1000);
        })
        .catch(error => {
            console.error("Error:", error);
            showAlert("Login failed: " + (error.message || "Unknown error"), "danger");
        })
        .finally(() => {
            hideSpinner();
        });
    });
});
