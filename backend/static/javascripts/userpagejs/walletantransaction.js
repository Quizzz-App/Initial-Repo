
const deposit = document.getElementById("deposit");
const withdrawal = document.getElementById("withdrawal");
const depositsettingspopup = document.querySelector(".depositsettingspopup");
const withdrawalsettingspopup = document.querySelector(".withdrawalsettingspopup");
const settingspopupclose = [...document.querySelectorAll("#settingspopupclose")];
const transactionTypeEl= document.getElementById("transactionType");
const transactionAmount= document.getElementById("transactionAmount");
const transactionEmail= document.getElementById("transactionEmail");
const transactionNumber= document.getElementById("transactionNumber");
const transactionNetwork= document.getElementById("transactionNetwork");
// const transactionAmount= document.getElementById("transactionAmount");

deposit.addEventListener('click',()=>{
   transactionTypeEl.value= "Deposit"
    depositsettingspopup.classList.toggle("active",true);
    body.style.overflow = "hidden"; 
});
withdrawal.addEventListener('click',()=>{
   transactionTypeEl.value= "Withdrawal"
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
   $.ajax({
      type: "POST",
      url: `/payment/store/`,
      data: {
         amount: transactionAmount.value,
         email: transactionEmail.value,
         contact: transactionNumber.value,
         payment_type: transactionTypeEl.value,
         carrier_code: transactionNetwork.options[transactionNetwork.selectedIndex].value,
         carrier_name: transactionNetwork.options[transactionNetwork.selectedIndex].text,
      },
      success: function (response) {
         if(response.code == 400){
            alertPopup(alert[1],response.msg);
         }else{
            window.location.href = '/payment/confirm/';
         }
      },
      error: function (response) {
        alertPopup(alert[1],"An error occurred");
      },
    });
})

initialwithdrawalbtn.addEventListener('click',()=>{
   let wAmount= document.getElementById("Wamount");
   let wNumber= document.getElementById("Wnumber");
   $.ajax({
      type: "POST",
      url: `/payment/issue-withdrawal/`,
      data: {
         amount: wAmount.value,
         acN: wNumber.value
      },
      success: function (response) {
         withdrawalsettingspopup.classList.toggle("active",false);
         body.style.overflow = "auto";
         alert(response.message);
      },
      error: function (response) {
        alert("An error occurred");
      },
    }); 
})