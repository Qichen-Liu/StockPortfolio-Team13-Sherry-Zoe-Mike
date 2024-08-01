labels = []
datasets_data = []

for(let i = 0; i < stocks_can_sell.length; i++) {
    labels.push(stocks_can_sell[i].stock_name);
    datasets_data.push(stocks_can_sell[i].quantity * stocks_can_sell[i].last_30_days_prices[0][1])
}

const data = {
    labels: labels,
    datasets: [{
      label: 'Total Value',
      data: datasets_data,
      backgroundColor: [
        'rgb(255, 99, 132)',
        'rgb(54, 162, 235)',
        'rgb(255, 205, 86)',
        'rgb(100, 205, 100)',
        'rgb(80, 107, 175)',
        'rgb(224,214,255)'
      ],
      hoverOffset: 4
    }]
};

new Chart(
    document.getElementById('piechart'),
    {
      type: 'doughnut',
      data: data
    }
);
