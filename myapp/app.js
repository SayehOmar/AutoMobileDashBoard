// app.js

const express = require('express');
const mongoose = require('mongoose');
const path = require('path'); 

const app = express();
const port = 3000; 
const indexRouter = require('./routes/index');

// MongoDB connection
const mongoDBUrl = 'mongodb://127.0.0.1:27017';
const dbName = 'Cars_data'; 


mongoose.connect(`${mongoDBUrl}/${dbName}`, {
    useNewUrlParser: true,
    useUnifiedTopology: true
})
.then(() => console.log('MongoDB Connected'))
.catch(err => console.error('MongoDB connection error:', err));



// Middleware
app.use(express.json());
app.use(express.urlencoded({ extended: false }));

// Serve static files from the public directory
app.use(express.static(path.join(__dirname, 'public')));

// Routes
app.use('/', indexRouter);

// Serve the HTML page
app.get('/', (req, res) => {
    res.sendFile(path.join(__dirname, 'public', 'index.html'));
});

// Start the server
app.listen(port, () => {
    console.log(`Server is running on http://localhost:${port}`);
});
