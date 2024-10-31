
const usermetview = [...document.getElementsByClassName("usermetview")];
const usermetholder = document.querySelector(".usermetholder");
const usermetpanelclose = document.getElementById("usermetpanelclose");

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