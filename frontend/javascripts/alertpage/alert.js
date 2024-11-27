
const alertbtn = [...document.getElementsByClassName("btn")];
const alert = [...document.getElementsByClassName("alert")];
const alertclose = [...document.getElementsByClassName("alertclose")];

alertbtn.forEach((alertbtn,ind)=>{
   alertbtn.addEventListener('click',()=>{
      alert[ind].classList.toggle("active");
   })
})

alertclose.forEach((alertclose,ind)=>{
   alertclose.addEventListener('click',()=>{
      alert[ind].classList.toggle("active",false);
   })
})