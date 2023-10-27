// FETCH DATA
fetch('/about/funding')
.then(response => response.json())
.then(areasData => {
  // Get canvas element
  const ctx = document.getElementById('funding');
  new Chart(ctx, {
    type: 'bar',
    data: {
      labels: Object.keys(areasData), // areasData keys as labels
      datasets: [{
        label: 'Funding Received',
        data: Object.values(areasData), // areasData values as data
        // One style used for all bars
        backgroundColor: 'rgba(99, 99, 200, 0.2)',
        borderColor: 'rgba(99, 99, 200, 1)',
        borderWidth: 1
      }]
    }, 
    options: {
      legend: {
        display: false // remove legend from view
      },
      scales: {
        xAxes: [{
          ticks: {
            autoSkip: false, // makes all x-labels viewable
            padding: 10
          },
          scaleLabel: {
            display: true,
            labelString: 'Areas of Gwent' // x-label
          }
        }],
        yAxes: [{
          ticks: {
            beginAtZero: true // forces y-axis to start at 0
          },
          scaleLabel: {
            display: true,
            labelString: 'Money Funded (£)' // y-label
          }
        }]
      }
    }
  });
})
.catch(e => console.log(e));
