import { renderTripsPerDay } from './charts/tripsPerDay.js';

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

// Run when page loads
document.addEventListener("DOMContentLoaded", () => {
  loadTripsPerDay();
});