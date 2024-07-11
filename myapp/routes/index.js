// routes/index.js

const express = require('express');
const router = express.Router();
const Car = require('../models/carModel');

// GET all cars
router.get('/cars', async (req, res) => {
    try {
        const cars = await Car.find({});
        res.json(cars);
    } catch (err) {
        res.status(500).json({ message: err.message });
    }
});

// POST a new car
router.post('/', async (req, res) => {
    const car = new Car({
        Brand: req.body.Brand,
        Model: req.body.Model,
        Manufacture_year: req.body.Manufacture_year,
        Mileage: req.body.Mileage,
        Price: req.body.Price,
        Body_type: req.body.Body_type,
        Fuel: req.body.Fuel,
        Horse_Power: req.body.Horse_Power,
        Gear_box: req.body.Gear_box,
        Transmission: req.body.Transmission,
        Announcement_date: req.body.Announcement_date,
        Governorate: req.body.Governorate,
        Address: req.body.Address,
        Shape_Leng: req.body.Shape_Leng,
        Shape_Area: req.body.Shape_Area,
        ADM2_EN: req.body.ADM2_EN
    });

    try {
        const newCar = await car.save();
        res.status(201).json(newCar);
    } catch (err) {
        res.status(400).json({ message: err.message });
    }
});

module.exports = router;
