const express = require('express');
const mysql = require('mysql2/promise');
const { ChartJSNodeCanvas } = require('chartjs-node-canvas');
require('dotenv').config();

const router = express.Router();

// MySQL connection pool
const pool = mysql.createPool({
    host: process.env.DB_HOST,
    port: process.env.DB_PORT,
    user: process.env.DB_USER,
    password: process.env.DB_PASS,
    database: process.env.DB_NAME,
});

// Chart settings
const width = 800; 
const height = 600;
const chartJSNodeCanvasInstance = new ChartJSNodeCanvas({ width, height });

// Function to generate the chart
async function generateTripsChart(tripsData){
    const configuration = {
        type: 'bar',
        data: {
            labels: tripsData.map(d => d.date),
            datasets: [{
                label: 'Total Trips per Day',
                data: tripsData.map(d => d.total_trips),
                backgroundColor: 'rgba(54, 162, 235, 0.6)',
            }]
        },
        options: {
            scales: {
                x: {title: {display: true, text: 'Date'} },
                y: {title: {display: true, text: 'Total Trips'} },
            }
        }
    };

    return chartJSNodeCanvasInstance.renderToBuffer(configuration);
}

// API endpoint to get trips per day chart
router.get('/get_trips_per_day', async (req, res) => {
    const query = `
    SELECT DATE(tpep_pickup_datetime) AS trip_date,
           COUNT(*) AS total_trips
    FROM trips
    GROUP BY trip_date
    ORDER BY trip_date;
    `;
    
    try {
        const [rows] = await pool.query(query);

        const data = rows.map(row => ({
            date: row.trip_date,
            total_trips: row.total_trips
        }));

        //Generate chart image
        const chartBuffer = await generateTripsChart(data);

        res.json({
            trips_per_day: data,
            chart_image: chartBuffer.toString('base64')
        });
    } catch (err) {
        console.error(err);
        res.status(500).json({ error: err.message});
    }
});


module.exports = router;
