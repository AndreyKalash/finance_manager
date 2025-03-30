var ctx1 = document.getElementById('sum_chart').getContext('2d');
var ctx2 = document.getElementById('count_chart').getContext('2d');


var myChart1 = new Chart(ctx1, {
    type: 'doughnut',
    data: {
      labels: ['Red', 'Blue', 'Yellow'],
      datasets: [{
        label: 'Суммарно потрачено',
        data: [12000, 19000, 3000],
        backgroundColor: [
          'rgba(255, 99, 132, 1)',
          'rgba(54, 162, 235, 1)',
          'rgba(255, 206, 86, 1)'
        ],
        borderColor: [
          'rgba(255, 99, 132, 1)',
          'rgba(54, 162, 235, 1)',
          'rgba(255, 206, 86, 1)'
        ],
        borderWidth: 1
      }]
    },
    options: {
      plugins: {
        datalabels: {
          color: '#fff', 
          font: {
            weight: 'bold',
            size: 14
          },
          formatter: (value) => {
            return (value / 1000).toFixed(2) + 'K';
          }
        }
      }
    },
    plugins: [ChartDataLabels]
  });
  

var myChart2 = new Chart(ctx2, {
    type: 'doughnut',
    data: {
      labels: ['Red', 'Blue', 'Yellow'],
      datasets: [{
        label: 'Суммарно куплено',
        data: [12, 19, 3],
        backgroundColor: [
          'rgba(255, 99, 132, 1)',
          'rgba(54, 162, 235, 1)',
          'rgba(255, 206, 86, 1)'
        ],
        borderColor: [
          'rgba(255, 99, 132, 1)',
          'rgba(54, 162, 235, 1)',
          'rgba(255, 206, 86, 1)'
        ],
        borderWidth: 1
      }]
    },
    options: {
      plugins: {
        datalabels: {
          color: '#fff',  // Color of the labels
          font: {
            weight: 'bold',
            size: 14
          },
          formatter: (value) => {
            // Convert value to thousands and format with two decimal places
            return value;
          }
        }
      }
    },
    plugins: [ChartDataLabels]
  });