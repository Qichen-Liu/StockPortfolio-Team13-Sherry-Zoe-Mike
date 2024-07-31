line_chart_labels = []
line_chart_datasets_data = []

for(let i = 0; i < stocks_can_sell[0].last_30_days_prices.length; i++) {
    line_chart_labels.push(stocks_can_sell[0].last_30_days_prices[i][0])
}


for(let i = 0; i < stocks_can_sell[0].last_30_days_prices.length; i++) {
    daily_worth = 0
    for(let j = 0; j < stocks_can_sell.length; j++) {
        daily_worth += stocks_can_sell[j].quantity * stocks_can_sell[j].last_30_days_prices[i][1] 
    }
    line_chart_datasets_data.push(daily_worth)
}


const line_chart_data = {
    labels: line_chart_labels.reverse(),
    datasets: [
        {
            label: "Net Worth",
            data: line_chart_datasets_data.reverse(),
            pointRadius: 5,
            pointHoverRadius: 15,
            fill: true
        }
    ]
}

new Chart(
    document.getElementById('linechart'),
    {
        type: 'line',
        data: line_chart_data,
        options: {
            interaction: {
                intersect: false,
            },
            plugins: {
                legend: {
                    display: false,
                }
            },
            scales: {
                x: {
                  grid: {
                    display: false,
                  }
                },
                y: {
                  border: {
                    display: false
                  },

                }
            }
        }
      
    }
    
);

