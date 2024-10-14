
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


const logoutbtn = document.getElementById("logoutbtn");
const logoutpopup = document.querySelector(".logoutpopup");
const confirmlogoutbtn = document.getElementById("confirmlogoutbtn");
const cancellogoutbtn = document.getElementById("cancellogoutbtn");

logoutbtn.addEventListener('click',()=>{
   logoutpopup.classList.toggle("active",true);
   body.style.overflow="hidden";
});
confirmlogoutbtn.addEventListener('click',()=>{
   window.location.href="/sitepages/loginpage/";
});
cancellogoutbtn.addEventListener('click',()=>{
   logoutpopup.classList.toggle("active",false);
   body.style.overflow="auto";
});