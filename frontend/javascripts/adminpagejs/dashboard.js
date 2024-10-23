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


   let graphfont = {
     family: "'Poppins', sans-serif",
     size: 16,
     weight: "600"
   }

  visitsChart = new Chart(ctx, {
    type: 'line',
    data: {
   labels: ['January','February','March','April','May','June','July','August','September','October','November','December'],
   datasets: [{
    data: [110, 200, 220, 160, 156, 211, 218, 250, 207, 364, 321, 300],
    fill: true,
    backgroundColor: stylecolor.getPropertyValue('--searchmolphcolor'),
    borderColor: stylecolor.getPropertyValue('--primitivecolor'),
    pointBorderColor: stylecolor.getPropertyValue('--secondarycolor'),
    borderWidth: 3,
    tension: 0.2
  }]
  },
    options: {
      responsive: true,
      layout: {
         padding: 30
     },
      plugins: {
      legend: {
         display: false
       },
    },
      scales: {
         x: {
            border: {
               display: true,
               color: stylecolor.getPropertyValue('--primitivecolor'),
               width: 4
            },
            grid: {
              display: false,
             },
            ticks: {
               color: stylecolor.getPropertyValue('--primitivecolor'),
               font: graphfont
            }
          },
        y: {
          beginAtZero: true,
          border: {
            display: true,
            color: stylecolor.getPropertyValue('--primitivecolor'),
            width: 4
          },
          grid: {
            display: false,
           },
           ticks: {
            color: stylecolor.getPropertyValue('--primitivecolor'),
            font: graphfont
          }
        }
      }
    }
  });

}

drawGraph();