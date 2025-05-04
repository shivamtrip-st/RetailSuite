const salesCtx = document.getElementById('salesChart').getContext('2d');
const salesChart = new Chart(salesCtx, {
    type: 'line',
    data: {
        labels: chartData.months,
        datasets: [{
            label: 'Sales',
            data: chartData.sales_data,
            backgroundColor: 'rgba(13, 110, 253, 0.1)',
            borderColor: 'rgba(13, 110, 253, 1)',
            borderWidth: 2,
            tension: 0.4,
            fill: true
        },
        ...(chartData.visitors_data ? [{
            label: 'Visitors',
            data: chartData.visitors_data,
            backgroundColor: 'rgba(25, 135, 84, 0.1)',
            borderColor: 'rgba(25, 135, 84, 1)',
            borderWidth: 2,
            tension: 0.4,
            fill: true
        }] : [])
        ]
    },
    options: {
        responsive: true,
        maintainAspectRatio: true,
        aspectRatio: 2,
        plugins: {
            legend: {
                position: 'top',
            }
        },
        scales: {
            y: {
                beginAtZero: true,
                grid: {
                    drawBorder: false
                }
            },
            x: {
                grid: {
                    display: false
                }
            }
        }
    }
});

// Category distribution Chart
const categoryCtx = document.getElementById('categoryChart').getContext('2d');
const categoryLabels = chartData.category_data.map(item => item.category__name);
const categoryCounts = chartData.category_data.map(item => item.count);
const categoryChart = new Chart(categoryCtx, {
    type: 'doughnut',
    data: {
        labels: categoryLabels,
        datasets: [{
            data: categoryCounts,
            backgroundColor: [
                'rgba(13, 110, 253, 0.8)',
                'rgba(220, 53, 69, 0.8)',
                'rgba(25, 135, 84, 0.8)',
                'rgba(255, 193, 7, 0.8)',
                'rgba(108, 117, 125, 0.8)'
            ],
            borderWidth: 0
        }]
    },
    options: {
        responsive: true,
        maintainAspectRatio: true,
        plugins: {
            legend: {
                position: 'right',
            }
        },
        cutout: '70%'
    }
});

// Review Sentiment Chart
const sentimentCtx = document.getElementById('reviewSentimentChart').getContext('2d');
const sentimentChart = new Chart(sentimentCtx, {
    type: 'pie',
    data: {
        labels: ['Positive', 'Neutral', 'Negative'],
        datasets: [{
            data: [
                chartData.review_sentiment.positive,
                chartData.review_sentiment.neutral,
                chartData.review_sentiment.negative
            ],
            backgroundColor: [
                'rgba(25, 135, 84, 0.8)',
                'rgba(108, 117, 125, 0.8)',
                'rgba(220, 53, 69, 0.8)'
            ],
            borderWidth: 0
        }]
    },
    options: {
        responsive: true,
        maintainAspectRatio: false,
        plugins: {
            legend: {
                position: 'bottom',
            },
            title: {
                display: true,
                text: 'Review Sentiment Distribution',
                font: {
                    size: 14,
                    weight: 'bold'
                }
            }
        }
    }
});

// Review Rating Chart
const ratingCtx = document.getElementById('reviewRatingChart').getContext('2d');
const ratingChart = new Chart(ratingCtx, {
    type: 'bar',
    data: {
        labels: ['1★', '2★', '3★', '4★', '5★'],
        datasets: [{
            label: 'Number of Reviews',
            data: chartData.rating_distribution,
            backgroundColor: 'rgba(13, 110, 253, 0.8)',
            borderWidth: 0,
            borderRadius: 4
        }]
    },
    options: {
        responsive: true,
        maintainAspectRatio: true,
        plugins: {
            legend: {
                display: false
            },
            title: {
                display: true,
                text: 'Review Rating Distribution',
                font: {
                    size: 14,
                    weight: 'bold'
                }
            }
        },
        scales: {
            y: {
                beginAtZero: true,
                grid: {
                    drawBorder: false
                }
            },
            x: {
                grid: {
                    display: false
                }
            }
        }
    }
});

// Time period selector functionality
document.getElementById('view-today').addEventListener('click', function () {
    updateTimeFrame('today');
    setActiveButton(this);
});

document.getElementById('view-week').addEventListener('click', function () {
    updateTimeFrame('week');
    setActiveButton(this);
});

document.getElementById('view-month').addEventListener('click', function () {
    updateTimeFrame('month');
    setActiveButton(this);
});

function setActiveButton(button) {
    document.querySelectorAll('.btn-group .btn').forEach(btn => {
        btn.classList.remove('active');
    });
    button.classList.add('active');
}

function updateTimeFrame(timeFrame) {
    console.log(`Fetching data for ${timeFrame} view`);

    if (timeFrame === 'today') {
        alert('In a real implementation, this would fetch today\'s data via AJAX');
    } else if (timeFrame === 'month') {
        alert('In a real implementation, this would fetch monthly data via AJAX');
    }
}
