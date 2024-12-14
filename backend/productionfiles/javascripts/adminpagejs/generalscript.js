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

modetoggle.addEventListener("click",()=>{
   const currentmode=body.getAttribute("data-theme");

   if(currentmode=="light"){
      body.setAttribute("data-theme","dark");
      modetoggle.innerHTML="light_mode";
      window.localStorage.setItem("QuizzAppTheme","dark");
   }else{
      body.setAttribute("data-theme","light");
      modetoggle.innerHTML="dark_mode";
      window.localStorage.setItem("QuizzAppTheme","light");
   }
});

//clickhandlers
const togglemenubar = document.getElementById("togglemenubar");
const menucontainer = document.querySelector(".menucontainer");

togglemenubar.addEventListener("click",()=>{
   menucontainer.classList.toggle("active");
   notificationscontainer.classList.toggle("active",false);
   forumcontainer.classList.toggle("active",false);
})



const logoutbtn = document.getElementById("logoutbtn");
const logoutpopup = document.querySelector(".logoutpopup");
const confirmlogoutbtn = document.getElementById("confirmlogoutbtn");
const cancellogoutbtn = document.getElementById("cancellogoutbtn");

logoutbtn.addEventListener('click',()=>{
   logoutpopup.classList.toggle("active",true);
   body.style.overflow="hidden";
});
confirmlogoutbtn.addEventListener('click',()=>{
   window.location.href="/accounts/logout-account";
});
cancellogoutbtn.addEventListener('click',()=>{
   logoutpopup.classList.toggle("active",false);
   body.style.overflow="auto";
});