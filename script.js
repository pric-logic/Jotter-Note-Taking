// Function to initialize Google Sign-In
function initGoogleSignIn() {
    gapi.load('auth2', function () {
        gapi.auth2.init({
            client_id: '507310393191-4bg4i9v3o2pq0bb5pdbdi2co7tnir6u7.apps.googleusercontent.com' // Replace with your client ID
        });
    });
}

// Function to handle successful sign-in
function onSignIn(googleUser) {
    // Get user profile information
    var profile = googleUser.getBasicProfile();
    console.log('ID: ' + profile.getId()); // Do not send this directly to your server!
    console.log('Name: ' + profile.getName());
    console.log('Image URL: ' + profile.getImageUrl());
    console.log('Email: ' + profile.getEmail());

    // Get authentication tokens
    var id_token = googleUser.getAuthResponse().id_token;
    console.log('ID Token: ' + id_token);

    // You can perform further actions here, such as sending the ID token to your server for verification
}

// Function to render Google Sign-In button
function renderGoogleSignInButton() {
    gapi.signin2.render('googleSignInButton', {
        'scope': 'profile email',
        'width': 200,
        'height': 40,
        'longtitle': true,
        'theme': 'dark',
        'onsuccess': onSignIn
    });
}

// Call initialization function when page loads
window.onload = function () {
    initGoogleSignIn();
};
