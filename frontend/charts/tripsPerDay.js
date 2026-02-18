export function renderTripsPerDay(data) {
  const ctx = document.getElementById("tripsPerDayChart").getContext("2d");

  // Extract labels (dates) and values (trip counts)
  const labels = data.map(item => item.date);
  const values = data.map(item => item.total_trips);

  new Chart(ctx, {
    type: "line",
    data: {
      labels: labels,
      datasets: [{
        label: "Trips per Day",
        data: values,
        borderColor: "blue",
        backgroundColor: "rgba(0, 0, 255, 0.1)",
        fill: true,
        tension: 0.3
      }]
    },
    options: {
      responsive: true,
      maintainAspectRatio: false,
      plugins: {
        legend: { display: true },
        title: { display: true, text: "NYC Trips per Day (Jan 1–12)" }
      },
      scales: {
        x: { title: { display: true, text: "Date" } },
        y: { title: { display: true, text: "Total Trips" } }
      }
    }
  });
}