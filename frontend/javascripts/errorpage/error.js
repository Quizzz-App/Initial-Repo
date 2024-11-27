//setTheme
const body=document.querySelector("body");
const modetoggle=document.getElementById("mode-toggle");

function settheme(){
    const currentmode=window.localStorage.getItem("QuizzAppTheme");

    if(currentmode=="dark"){
      body.setAttribute("data-theme","dark");
      modetoggle.innerHTML="light_mode";
      window.localStorage.setItem("QuizzAppTheme","dark");
   }else{
      body.setAttribute("data-theme","light");
      modetoggle.innerHTML="dark_mode";
      window.localStorage.setItem("QuizzAppTheme","light");
   }
}
settheme();