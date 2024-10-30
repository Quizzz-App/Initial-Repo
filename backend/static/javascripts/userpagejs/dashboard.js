const modetogge=document.getElementById("mode-toggle");

modetogge.addEventListener("click",()=>{
   drawGraph();
});

var earningsChart;
var referralChart;

function drawGraph(){

   const stylecolor =  getComputedStyle(body);
   const ctx = document.getElementById('myChart');
   const ctx2 = document.getElementById('myChart2');

   if(earningsChart!=0){
      earningsChart?.destroy();
   }

   if(referralChart!=0){
      referralChart?.destroy();
   }

   let graphfont = {
    family: "'Poppins', sans-serif",
    size: 16,
    weight: "600"
  }

  earningsChart = new Chart(ctx, {
    type: 'line',
    data: {
  labels: ['March','April','May','June','July'],
  datasets: [{
    label: 'GH₵',
    data: [20, 81, 96, 55, 56],
    fill: true,
    borderColor: stylecolor.getPropertyValue('--primitivecolor'),
    pointBorderColor: stylecolor.getPropertyValue('--secondarycolor'),
    borderWidth: 2,
    tension: 0.2
  }]
  },
    options: {
      layout: {
        padding: 10
    },
      plugins: {
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
               color: stylecolor.getPropertyValue('--primitivecolor'),
               font: graphfont
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
            color: stylecolor.getPropertyValue('--primitivecolor'),
            font: graphfont
          }
        }
      }
    }
  });

  referralChart = new Chart(ctx2, {
    type: 'bar',
    data: {
      labels: ['Feb','March','April','May','June'],
      datasets: [{
        label: 'Referrals',
        data: [6, 13, 9, 10, 5],
        borderWidth: 2,
        borderRadius: 10,
        borderColor: stylecolor.getPropertyValue('--secondarycolor'),
        backgroundColor: stylecolor.getPropertyValue('--primitivecolor')
      }]
    },
    options: {
      layout: {
        padding: 10
     },
      plugins: {
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
               color: stylecolor.getPropertyValue('--primitivecolor'),
               font: graphfont
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
            color: stylecolor.getPropertyValue('--primitivecolor'),
            font: graphfont
          }
        }
      }
    }
  });

}

drawGraph();