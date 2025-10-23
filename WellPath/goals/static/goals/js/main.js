document.addEventListener('DOMContentLoaded', function () {
  const canvas = document.getElementById('progressChart');
  if (!canvas) return;
  const ctx = canvas.getContext('2d');

  const jsonEl = document.getElementById('chart-data');
  const chartData = JSON.parse(jsonEl.textContent);

  const target = Number(chartData.target) || 0;
  const avg = Number(chartData.avg_per_day) || 0;
  const grouping = chartData.grouping || 'daily';

  // Determine appropriate label based on grouping
  let xAxisLabel = 'Date';
  if (grouping === 'weekly') {
    xAxisLabel = 'Week';
  } else if (grouping === 'monthly') {
    xAxisLabel = 'Month';
  }

  // Determine y-axis label based on grouping
  let valueLabel = 'Daily Progress';
  if (grouping === 'weekly') {
    valueLabel = 'Weekly Progress';
  } else if (grouping === 'monthly') {
    valueLabel = 'Monthly Progress';
  }

  new Chart(ctx, {
    type: 'line',
    data: {
      labels: chartData.dates,
      datasets: [
        {
          label: 'Cumulative Total',
          data: chartData.cumulative,
          borderColor: '#007bff',
          backgroundColor: 'rgba(0,123,255,0.15)',
          borderWidth: 3,
          tension: 0.1,
          fill: false,
          pointRadius: 3,
          pointHoverRadius: 5
        },
        {
          label: valueLabel,
          data: chartData.values,
          borderColor: '#28a745',
          backgroundColor: 'rgba(40,167,69,0.2)',
          borderWidth: 2,
          tension: 0.3,
          fill: true,
          pointRadius: 3,
          pointHoverRadius: 5
        },
        {
          label: 'Target',
          data: new Array(chartData.dates.length).fill(target),
          borderColor: '#dc3545',
          borderWidth: 2,
          borderDash: [6, 6],
          pointRadius: 0,
          fill: false
        }
      ]
    },
    options: {
      responsive: true,
      maintainAspectRatio: false,
      interaction: {
        mode: 'index',
        intersect: false,
      },
      plugins: { 
        legend: { 
          position: 'bottom',
          labels: {
            usePointStyle: true,
            padding: 15
          }
        },
        tooltip: {
          callbacks: {
            label: function(context) {
              let label = context.dataset.label || '';
              if (label) {
                label += ': ';
              }
              if (context.parsed.y !== null) {
                label += context.parsed.y.toFixed(2) + ' ' + (chartData.unit || '');
              }
              return label;
            }
          }
        }
      },
      scales: {
        y: {
          beginAtZero: true,
          title: { 
            display: true, 
            text: chartData.unit || 'Progress',
            font: {
              size: 13,
              weight: 'bold'
            }
          },
          ticks: {
            callback: function(value) {
              return value.toFixed(0);
            }
          }
        },
        x: {
          title: { 
            display: true, 
            text: xAxisLabel,
            font: {
              size: 13,
              weight: 'bold'
            }
          },
          ticks: {
            maxRotation: 45,
            minRotation: 0,
            autoSkip: true,
            maxTicksLimit: grouping === 'daily' ? 30 : (grouping === 'weekly' ? 20 : 12)
          }
        }
      }
    }
  });


});
