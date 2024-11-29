
const alertbtn = [...document.getElementsByClassName("btn")];
const alert = [...document.getElementsByClassName("alert")];
const alertclose = [...document.getElementsByClassName("alertclose")];

// alertbtn.forEach((alertbtn,ind)=>{
//    alertbtn.addEventListener('click',()=>{
//       alert[ind].classList.toggle("active");
//    })
// })

const successAlert= alert[0]
const errorAlert= alert[1]

function alertPopup(alert, message){
   alert.querySelector(".alertmsg").textContent= message
   alert.classList.toggle("active")
}

alertclose.forEach((alertclose,ind)=>{
   alertclose.addEventListener('click',()=>{
      alert[ind].classList.toggle("active",false);
   })
})