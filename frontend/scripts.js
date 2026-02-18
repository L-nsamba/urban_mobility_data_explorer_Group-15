import { renderTripsPerDay } from './charts/tripsPerDay.js';
import { renderTopRushHours } from './charts/rushHours.js';
import { renderAverageSpeedPerDay } from './charts/avgSpeedPerDayPerBorough.js';

async function loadTripsPerDay() {
  try {
    const response = await fetch("http://localhost:5000/api/get_trips_per_day");
    const json = await response.json();

    // Pass the data to Chart.js renderer
    renderTripsPerDay(json.trips_per_day);
  } catch (err) {
    console.error("Error fetching trips per day:", err);
  }
}

  // New function to load average speed per day data
async function loadAverageSpeedPerDay() {
  try {
    const response = await fetch("http://localhost:5000/api/get_avg_speed_per_day");
    const json = await response.json();

    // Pass the data to Chart.js renderer
    renderAverageSpeedPerDay(json.avg_speed_per_day);
  } catch (err) {
    console.error("Error fetching average speed per day:", err);
  }
}

// Run when page loads
document.addEventListener("DOMContentLoaded", () => {
  loadTripsPerDay();
});

document.addEventListener("DOMContentLoaded", () => {
  loadAverageSpeedPerDay();
});

document.addEventListener("DOMContentLoaded", () => {
  // Values we obtained from running the frequency.py dsa test
  const topRushHours = [
    { hour: "18 (6pm)", total_trips:167358 },
    { hour: "17 (5pm)", total_trips:153606 },
    { hour: "19 (7pm)", total_trips:153991 },
    { hour: "15 (3pm)", total_trips:149747 },
    { hour: "14 (2pm)", total_trips:142505 }
  ];

  renderTopRushHours(topRushHours);
})