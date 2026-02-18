export function renderAverageSpeedPerDay(data) {
  const ctx = document.getElementById("averageSpeedChart").getContext("2d");

  // Extract labels (dates) and values (average speeds) from the data
  const labels = data.map(item => item.date);
  const values = data.map(item => item.avg_speed_kmh);

  new Chart(ctx, {
    type: "line",
    data: {
      labels: labels,
      datasets: [{
        label: "Average Trip Speed per Day",
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
        title: { display: true, text: "NYC Trips' average speed per Day (Jan 1–12)" }
      },
      scales: {
        x: { title: { display: true, text: "Date" } },
        y: { title: { display: true, text: "Average Trip speed" } }
      }
    }
  });
}