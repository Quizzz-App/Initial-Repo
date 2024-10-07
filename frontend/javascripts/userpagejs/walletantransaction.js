
const deposit = document.getElementById("deposit");
const withdrawal = document.getElementById("withdrawal");
const depositsettingspopup = document.querySelector(".depositsettingspopup");
const withdrawalsettingspopup = document.querySelector(".withdrawalsettingspopup");
const settingspopupclose = [...document.querySelectorAll("#settingspopupclose")];

deposit.addEventListener('click',()=>{
    depositsettingspopup.classList.toggle("active",true);
});
withdrawal.addEventListener('click',()=>{
   withdrawalsettingspopup.classList.toggle("active",true);
});
settingspopupclose[0].addEventListener('click',()=>{
   depositsettingspopup.classList.toggle("active",false);
});
settingspopupclose[1].addEventListener('click',()=>{
   withdrawalsettingspopup.classList.toggle("active",false);
});