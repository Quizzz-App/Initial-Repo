const modetogge=document.getElementById("mode-toggle");



var earningsChart;
var referralChart;

function drawGraph(monthsData, earninData, referalData){

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
  labels: monthsData,
  datasets: [{
    label: 'GH₵',
    data: earninData,
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
      labels: monthsData,
      datasets: [{
        label: 'Referrals',
        data: referalData,
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

fetch('/ref/get-ref-analytics/')
.then(response => response.json())
.then(response => {
  let months= [];
  let earninData= [];
  let referalData= [];
  for (month in response){
    months.push(month);
    earninData.push(Math.round(parseFloat((response[month]['refEarn'])) * 100) / 100);
    referalData.push(response[month]['refAmount']);
  }
  modetogge.addEventListener("click",()=>{
    drawGraph(months, earninData, referalData);
 });
 drawGraph(months, earninData, referalData);
})
