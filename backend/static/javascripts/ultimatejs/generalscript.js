

function settheme(){
   const body=document.querySelector("body");
    const currentmode=window.localStorage.getItem("QuizzAppTheme");

    if(currentmode=="dark"){
      body.setAttribute("data-theme","dark");
      window.localStorage.setItem("QuizzAppTheme","dark");
   }else{
      body.setAttribute("data-theme","light");
      window.localStorage.setItem("QuizzAppTheme","light");
   }
}

settheme();



