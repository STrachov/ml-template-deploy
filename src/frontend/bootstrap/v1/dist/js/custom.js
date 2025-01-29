
//Handle the spinner
function showSpinner() {
    document.getElementById('spinner-backdrop').style.display = 'flex';
}

function hideSpinner() {
    document.getElementById('spinner-backdrop').style.display = 'none';
}
function hidePreloader() {
    document.querySelector('.preloader').style.display = 'none';
}
function showAlert(text="", mode="success", alertID="session_param_alert"){
  const alertHTML = '<div class="alert customize-alert alert-dismissible border-'+mode+' text-'+mode+' fade show remove-close-icon" role="alert">\n' +
      '                      <button type="button" class="btn-close" data-bs-dismiss="alert" aria-label="Close"></button>\n' +
      '                      <div class="d-flex align-items-center font-medium me-3 me-md-0">\n' +
      '                        <i class="ti ti-info-circle fs-5 me-2 text-'+mode+'"></i>\n' +
                              text +
      '                      </div>\n' +
      '                    </div>'
  const alertElement = document.getElementById(alertID)
  alertElement.innerHTML = alertHTML
}

hidePreloader();


async function loadConfig() {
    try {
        const response = await fetch("./dist/config.json");  // Load config file

        if (!response.ok) {
            throw new Error(`HTTP error! Status: ${response.status}`);
        }

        const config = await response.json();  // Parse JSON

        console.log("Config loaded successfully:", config);
        return config;  // Return config object
    } catch (error) {
        console.error("Error loading config:", error);

        // Fallback config in case of failure
        return {
            base_url: "http://localhost:8080/api/v1"
        };
    }
}
let base_url = "";

// async function initApp() {
//     const config = await loadConfig();
//     base_url = config.base_url;  // Set global variable
//     console.log("Base URL Loaded:", base_url);
// }

(async function init() {
    window.base_url = (await loadConfig()).base_url;
    console.log("Global window.base_url initialized:", window.base_url);

})();


function refreshToken() {
    console.log("Refreshing access token...");

    return fetch(`${window.base_url}/refresh-token`, {
        method: "POST",
        credentials: "include"  // ✅ Includes cookies in the request
    })
    .then(response => {
        if (!response.ok) {
            throw new Error("Failed to refresh token");
        }
        return response.json();
    })
    .then(data => {
        console.log("Access token refreshed.");
        return true;
    })
    .catch(error => {
        console.error("Error refreshing token:", error);
        return false;
    });
}


async function testToken() {
    console.log("Checking authentication status...",window.base_url);
    try {
        // Attempt to refresh token before checking session
        const refreshed = await refreshToken();
        if (!refreshed) {
            throw new Error("Session expired. Please log in again.");
        }

        const response = await fetch(`${window.base_url}/login/test-token`, {
            method: "POST",
            credentials: "include"  // Includes cookies in request
        });

        if (!response.ok) {
            throw new Error("Unauthorized");
        }
        const userData = await response.json();
        console.log("Authenticated User Data:", userData);
        return userData;
    } catch (error) {
        console.error("Session expired or invalid:", error);
    }
}