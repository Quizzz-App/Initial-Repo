
const usermetview = [...document.getElementsByClassName("usermetview")];
const usermetholder = document.querySelector(".usermetholder");
const usermetpanelclose = document.getElementById("usermetpanelclose");

const deactivatereqview = [...document.getElementsByClassName("deactivatereqview")];
const deactivationreqholder = document.querySelector(".deactivationreqholder");
const deactivationreqpanelclose = document.getElementById("deactivationreqpanelclose");

usermetview.forEach((usermet,i)=>{
   usermet.addEventListener('click',()=>{
      usermetholder.classList.toggle("active",true);
      body.style.overflowY="hidden";
   })
})
usermetpanelclose.addEventListener('click',()=>{
   usermetholder.classList.toggle("active",false);
   body.style.overflowY="auto";
})

deactivatereqview.forEach((reqdetail,i)=>{
   reqdetail.addEventListener('click',()=>{
      deactivationreqholder.classList.toggle("active",true);
      body.style.overflowY="hidden";
   })
})
deactivationreqpanelclose.addEventListener('click',()=>{
   deactivationreqholder.classList.toggle("active",false);
   body.style.overflowY="auto";
})