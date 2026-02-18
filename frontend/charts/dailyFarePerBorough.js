let fareChartInstance = null;

export function renderFarePerDayPerBorough(data) {
    const canvas = document.getElementById("dailyFareChart");
    if (!canvas) {
        console.error("Canva with id='dailyFareChart' not found.");
        return;
    }

    const ctx = canvas.getContext("2d");

    const dates = [...new Set(data.map(item => item.date))].sort();
    const boroughs = [...new Set(data.map(item => item.borough))].sort();

    const datasets = boroughs.map((borough) => {
        const values = dates.map((date) => {
            const row = data.find(d => d.date === date && d.borough === borough);
            return row ? row.total_fare : 0;
        });

        return {
            label: borough,
            data: values,
            borderwidth: 1
        }
    });

    // To avoid an overlap of charts, we destroy any previous chart existing to allow a new fetch from the API and rendering
    if (fareChartInstance) {
        fareChartInstance.destroy();
    }

    fareChartInstance = new Chart(ctx, {
        type: "bar",
        data: {
            labels: dates,
            datasets: datasets
        },
        options : {
            response: true,
            maintainAspectRation: false,
            plugins: {
                legend: { display: true },
                title: {display: true, text: "Daily Total Fare per Borough"}
            },
            scales: {
                x: {
                    stacked: true,
                    title: { display: true, text: "Date"}
                },
                y: {
                    stacked: true,
                    title: {display: true, text: "Total Fare (SUM total_amount)" },
                    beginAtZero: true
                }
            }
        }
    });
}

