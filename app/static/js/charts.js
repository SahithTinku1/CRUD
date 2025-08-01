document.addEventListener("DOMContentLoaded", function () {
    // Pie Chart (Category)
    const catCtx = document.getElementById('categoryChart');
    if (catCtx) {
        const categoryChart = new Chart(catCtx, {
            type: 'pie',
            data: {
                labels: JSON.parse(catCtx.dataset.labels),
                datasets: [{
                    label: 'Expenses',
                    data: JSON.parse(catCtx.dataset.totals),
                    backgroundColor: [
                        '#4e79a7', '#f28e2b', '#e15759',
                        '#76b7b2', '#59a14f', '#edc949'
                    ]
                }]
            },
            options: {
                responsive: true,
                plugins: {
                    legend: {
                        position: 'bottom',
                        labels: {
                            color: 'white'
                        }
                    },
                    tooltip: {
                        bodyColor: 'white',
                        titleColor: 'white'
                    }
                }
            }
        });
    }

    // Bar Chart (Monthly)
    const monthCtx = document.getElementById('monthlyChart');
    if (monthCtx) {
        const monthlyChart = new Chart(monthCtx, {
            type: 'bar',
            data: {
                labels: JSON.parse(monthCtx.dataset.labels),
                datasets: [{
                    label: 'Monthly Spending',
                    data: JSON.parse(monthCtx.dataset.totals),
                    backgroundColor: '#4e79a7'
                }]
            },
            options: {
                responsive: true,
                scales: {
                    y: {
                        beginAtZero: true,
                        ticks: {
                            color: 'white'
                        }
                    },
                    x: {
                        ticks: {
                            color: 'white'
                        }
                    }
                },
                plugins: {
                    legend: {
                        labels: {
                            color: 'white'
                        }
                    },
                    tooltip: {
                        bodyColor: 'white',
                        titleColor: 'white'
                    }
                }
            }
        });
    }
});
