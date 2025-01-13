const express = require('express');
const sqlite3 = require('sqlite3').verbose();
const multer = require('multer');
const bcrypt = require('bcrypt');
const bodyParser = require('body-parser');
const cors = require('cors'); // Import CORS
const path = require('path');

const app = express();
const db = new sqlite3.Database('users.db'); // Use a file-based SQLite database

// Middleware
app.use(cors()); // Enable CORS
app.use(bodyParser.urlencoded({ extended: true })); // Handle URL-encoded data
app.use(bodyParser.json()); // Handle JSON data
app.use(express.static('public')); // Serve static files from the public directory

// Set up multer for file uploads
const storage = multer.diskStorage({
    destination: (req, file, cb) => {
        cb(null, 'uploads/'); // Specify the upload directory
    },
    filename: (req, file, cb) => {
        cb(null, Date.now() + path.extname(file.originalname)); // Append timestamp to the filename
    }
});

const upload = multer({ storage: storage });

// Create users table if it doesn't exist
db.serialize(() => {
    db.run("CREATE TABLE IF NOT EXISTS users (id INTEGER PRIMARY KEY AUTOINCREMENT, firstName TEXT, lastName TEXT, email TEXT UNIQUE, password TEXT, grade TEXT, careerInterest TEXT, aboutYourself TEXT, resume TEXT)");
});

// Register endpoint
app.post('/register', upload.single('resume'), (req, res) => {
    const { firstName, lastName, email, password, grade, careerInterest, aboutYourself } = req.body;
    const hashedPassword = bcrypt.hashSync(password, 8);
    const resumePath = req.file ? req.file.path : null; // Get the path of the uploaded file

    db.run("INSERT INTO users (firstName, lastName, email, password, grade, careerInterest, aboutYourself, resume) VALUES (?, ?, ?, ?, ?, ?, ?, ?)", 
    [firstName, lastName, email, hashedPassword, grade, careerInterest, aboutYourself, resumePath], function(err) {
        if (err) {
            return res.status(500).json({ success: false, message: "Error registering user." });
        }
        res.status(201).json({ success: true, message: "User  registered successfully!" });
    });
});

// Start the server
app.listen(3000, () => {
    console.log('Server is running on port 3000');
});