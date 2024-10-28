
const deposit = document.getElementById("deposit");
const withdrawal = document.getElementById("withdrawal");
const depositsettingspopup = document.querySelector(".depositsettingspopup");
const withdrawalsettingspopup = document.querySelector(".withdrawalsettingspopup");
const settingspopupclose = [...document.querySelectorAll("#settingspopupclose")];

deposit.addEventListener('click',()=>{
    depositsettingspopup.classList.toggle("active",true);
    body.style.overflow = "hidden"; 
});
withdrawal.addEventListener('click',()=>{
   withdrawalsettingspopup.classList.toggle("active",true);
   body.style.overflow = "hidden"; 
});
settingspopupclose[0].addEventListener('click',()=>{
   depositsettingspopup.classList.toggle("active",false);
   body.style.overflow = "auto"; 
});
settingspopupclose[1].addEventListener('click',()=>{
   withdrawalsettingspopup.classList.toggle("active",false);
   body.style.overflow = "auto"; 
});

const initialdepositbtn = document.getElementById("initialdepositbtn");
const initialwithdrawalbtn = document.getElementById("initialwithdrawalbtn");

initialdepositbtn.addEventListener('click',()=>{
   window.location.href = "/../sitepages/auxilliarypages/paymentpage/";
})

initialwithdrawalbtn.addEventListener('click',()=>{
   window.location.href = "/../sitepages/auxilliarypages/paymentpage/";
})