const modetogge=document.getElementById("mode-toggle");

modetogge.addEventListener("click",()=>{
   drawGraph();
});

var visitsChart;

function drawGraph(){

   const stylecolor =  getComputedStyle(body);
   const ctx = document.getElementById('myChart');

   if(visitsChart!=0){
      visitsChart?.destroy();
   }

  visitsChart = new Chart(ctx, {
    type: 'line',
    data: {
  labels: ['March','April','May','June','July'],
  datasets: [{
    label: 'GH₵',
    data: [20, 81, 96, 55, 56],
    fill: false,
    borderColor: stylecolor.getPropertyValue('--primitivecolor'),
    pointBorderColor: stylecolor.getPropertyValue('--secondarycolor'),
    borderWidth: 2,
    tension: 0.5
  }]
  },
    options: {
      plugins: {
      title: {
        display: true,
        text: 'Earnings (Last 5 Months)'
      },
      legend: {
         display: false,
       },
    },
      scales: {
         x: {
            border: {
               display: true,
               color: stylecolor.getPropertyValue('--primitivecolor'),
               width: 3
            },
            grid: {
              display: false,
             },
             ticks: {
               color: stylecolor.getPropertyValue('--primitivecolor')
             }
          },
        y: {
          beginAtZero: true,
          border: {
            display: true,
            color: stylecolor.getPropertyValue('--primitivecolor'),
            width: 3
          },
          grid: {
            display: false,
           },
           ticks: {
            color: stylecolor.getPropertyValue('--primitivecolor')
          }
        }
      }
    }
  });

}

drawGraph();