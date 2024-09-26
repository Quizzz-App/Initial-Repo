
//setTheme
const body=document.querySelector("body");

function settheme(){
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

const modetoggle=document.getElementById("mode-toggle");

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


//clickhandlers
const togglemenubar = document.getElementById("togglemenubar");
const menucontainer = document.querySelector(".menucontainer");
const togglenotification = document.getElementById("notification-toggle");
const notificationscontainer = document.querySelector(".notificationscontainer");
const forumtoggle = document.getElementById("forum-toggle");
const forumcontainer = document.querySelector(".forumcontainer");
const composesection = document.querySelector(".composesection");
const togglechallenge = document.getElementById("togglechallenge");
const cancelchallenge = document.getElementById("cancelchallenge");

togglemenubar.addEventListener("click",()=>{
   menucontainer.classList.toggle("active");
   notificationscontainer.classList.toggle("active",false);
   forumcontainer.classList.toggle("active",false);
})

togglenotification.addEventListener("click",()=>{
   menucontainer.classList.toggle("active",false);
   notificationscontainer.classList.toggle("active");
   forumcontainer.classList.toggle("active",false);
})

forumtoggle.addEventListener("click",()=>{
   menucontainer.classList.toggle("active",false);
   notificationscontainer.classList.toggle("active",false);
   forumcontainer.classList.toggle("active");
})

togglechallenge.addEventListener("click",()=>{
   composesection.classList.toggle("composechallenge",true);
})
cancelchallenge.addEventListener("click",()=>{
   composesection.classList.toggle("composechallenge",false);
})