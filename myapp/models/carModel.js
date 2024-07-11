// models/carModel.js

const mongoose = require('mongoose');

const carSchema = new mongoose.Schema({
    Brand: String,
    Model: String,
    Manufacture_year: Number,
    Mileage: String,
    Price: String,
    Body_type: String,
    Fuel: String,
    Horse_Power: String,
    Gear_box: String,
    Transmission: String,
    Announcement_date: String,
    Governorate: String,
    Address: String,
    Shape_Leng: Number,
    Shape_Area: Number,
    ADM2_EN: String
},{collection:'Cars_data'});

const Car = mongoose.model('Car', carSchema);

module.exports = Car;
