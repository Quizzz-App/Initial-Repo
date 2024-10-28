const modetoggle=document.getElementById("mode-toggle");
const body=document.querySelector("body");

modetoggle.addEventListener("click",()=>{
   const currentmode=body.getAttribute("data-theme");

   if(currentmode=="light"){
      body.setAttribute("data-theme","dark");
      modetoggle.innerHTML="dark_mode";
      window.localStorage.setItem("QuizzAppTheme","dark");
   }else{
      body.setAttribute("data-theme","light");
      modetoggle.innerHTML="light_mode";
      window.localStorage.setItem("QuizzAppTheme","light");
   }
});