const modetogge=document.getElementById("mode-toggle");

modetogge.addEventListener("click",()=>{
   drawSignUPGraph();
   drawVisitsGraph();
});


function drawSignUPGraph(){

  var monthlyChart;
  var yearlyChart;

   const stylecolor =  getComputedStyle(body);
   const ctx = document.getElementById('signUpmonthlyChart');
   const ctx2 = document.getElementById('signUpyearlyChart');

   if(monthlyChart!=0){
      monthlyChart?.destroy();
   }

   if(yearlyChart!=0){
      yearlyChart?.destroy();
   }

   let graphfont = {
    family: "'Poppins', sans-serif",
    size: 16,
    weight: "600"
  }

  monthlyChart = new Chart(ctx, {
    type: 'line',
    data: {
  labels: ['March','April','May','June','July'],
  datasets: [{
    label: 'TSU',
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


  yearlyChart = new Chart(ctx2, {
   type: 'line',
   data: {
 labels: ['2020','2021','2022','2023','2024'],
 datasets: [{
   label: "TSU",
   data: [121, 132, 100, 156, 200],
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

}

function drawVisitsGraph(){

  var monthlyChart;
  var yearlyChart;

   const stylecolor =  getComputedStyle(body);
   const ctx = document.getElementById('visitsmonthlyChart');
   const ctx2 = document.getElementById('visitsyearlyChart');

   if(monthlyChart!=0){
      monthlyChart?.destroy();
   }

   if(yearlyChart!=0){
      yearlyChart?.destroy();
   }

   let graphfont = {
    family: "'Poppins', sans-serif",
    size: 16,
    weight: "600"
  }

  monthlyChart = new Chart(ctx, {
    type: 'line',
    data: {
  labels: ['March','April','May','June','July'],
  datasets: [{
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


  yearlyChart = new Chart(ctx2, {
   type: 'line',
   data: {
 labels: ['2020','2021','2022','2023','2024'],
 datasets: [{
   label: "TSU",
   data: [121, 132, 100, 156, 200],
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

}

drawSignUPGraph();
drawVisitsGraph();