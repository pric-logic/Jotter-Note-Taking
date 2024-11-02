<?php
// Configuration
$db_host = 'localhost';
$db_username = 'root';
$db_password = '';
$db_name = 'jotter';

// Create connection
$conn = new mysqli($db_host, $db_username, $db_password, $db_name);

// Check connection
if ($conn->connect_error) {
    die("Connection failed: ". $conn->connect_error);
}

// Get form data
$username = $_POST['username'];
$email = $_POST['email'];
$password = $_POST['password'];
$confirm_password = $_POST['confirm_password'];

// Validate form data
if ($password!= $confirm_password) {
    echo "Passwords do not match";
    exit;
}

// Hash password
$password_hash = password_hash($password, PASSWORD_DEFAULT);

// Insert data into database
$query = "INSERT INTO users (username, email, password) VALUES ('$username', '$email', '$password_hash')";
if ($conn->query($query) === TRUE) {
    echo "New record created successfully";
    header('Location: home.html'); // Redirect to home.html
    exit;
} else {
    echo "Error: ". $query. "<br>". $conn->error;
}

$conn->close();
?>