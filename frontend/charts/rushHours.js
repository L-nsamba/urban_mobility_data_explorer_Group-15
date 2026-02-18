export function renderTopRushHours(data) {
    const ctx = document.getElementById("rushHoursChart").getContext("2d");

    // Extracting hours and trip counts
    const labels = data.map(item => `Hour ${item.hour}`);
    const values = data.map(item => item.total_trips);

    new Chart(ctx, {
        type: "pie",
        data: {
            labels: labels,
            datasets: [{
                label: "Top 5 Rush Hours",
                data: values,
                backgroundColor: [
                    "rgba(255, 99, 132, 0.6)",
                    "rgba(54, 162, 235, 0.6)",
                    "rgba(255, 206, 86, 0.6)",
                    "rgba(75, 192, 192, 0.6)",
                    "rgba(153, 102, 255, 0.6)"
                ]
            }]
        },
        options: {
            responsive: true,
            plugins: {
                legend: {position: "right"},
                title: {display: true, text: "Top 5 Rush Hours"}
            }
        }
    })
}