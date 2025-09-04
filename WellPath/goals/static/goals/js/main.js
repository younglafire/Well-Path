document.addEventListener('DOMContentLoaded', function () {
  const canvas = document.getElementById('progressChart');
  if (!canvas) return;
  const ctx = canvas.getContext('2d');

  const jsonEl = document.getElementById('chart-data');
  const chartData = JSON.parse(jsonEl.textContent);

  const target = Number(chartData.target) || 0;
  const avg = Number(chartData.avg_per_day) || 0;

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
          borderWidth: 2,
          tension: 0,
          fill: false,
          pointRadius: 2
        },
        {
          label: 'Daily Progress',
          data: chartData.values,
          borderColor: '#28a745',
          backgroundColor: 'rgba(40,167,69,0.15)',
          borderWidth: 2,
          tension: 0.3,
          fill: false,
          pointRadius: 2
        },
        {
          label: 'Target',
          data: new Array(chartData.dates.length).fill(target),
          borderColor: 'red',
          borderWidth: 2,
          borderDash: [6, 6],
          pointRadius: 0,
          fill: false
        },
        {
          label: 'Average So Far',
          data: new Array(chartData.dates.length).fill(avg),
          borderColor: 'orange',
          borderWidth: 2,
          borderDash: [2, 6],
          pointRadius: 0,
          fill: false
        }
      ]
    },
    options: {
      responsive: true,
      maintainAspectRatio: false,
      plugins: { legend: { position: 'bottom' } },
      scales: {
        y: {
          beginAtZero: true,
          max: target,   // hard ceiling = target
          title: { display: true, text: chartData.unit || '' }
        },
        x: {
          title: { display: true, text: 'Date' }
        }
      }
    }
  });


});
