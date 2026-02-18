export function renderTripsPerHour(data) {
    const ctx = document.getElementById("tripsPerHourChart").getContext("2d");

    // Extract labels (dates) and values (trip counts)
    const labels = data.map(item => item.hour);
    const values = data.map(item => item.total_trips);

    new Chart(ctx, {
        type: "bar",
        data: {
            labels: labels,
            datasets: [{
                label: "Trips per Hour",
                data: values,
                backgroundColor: "rgba(153, 102, 255, 0.6)",
                fill: true,
                tension: 0.3
            }]
        },
        options: {
            responsive: true,
            maintainAspectRatio: false,
            plugins: {
                legend: { display: true },
                title: { display: true, text: "NYC Trips per Hour(0-23)" }
            },
            scales: {
                x: { title: { display: true, text: "Hours" } },
                y: { title: { display: true, text: "Total Trips" } }
            }
        }
    });
}