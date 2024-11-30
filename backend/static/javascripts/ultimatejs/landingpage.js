const modetoggle=document.getElementById("mode-toggle");
const body=document.querySelector("body");

try {
   const msg= document.querySelector('.message')
   if(msg.classList.contains('error')){
     alertPopup(alert[1], msg.textContent)
   }else if(msg.classList.contains('success')){
     alertPopup(alert[0], msg.textContent)
   }
 } catch (error) {
   
 }
 

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