
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
   console.log(transactionNetwork.options[transactionNetwork.selectedIndex].text)
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
         window.location.href = '/payment/confirm/';
      },
      error: function (response) {
        alert("An error occurred");
      },
    });
})

initialwithdrawalbtn.addEventListener('click',()=>{
   window.location.href = "/../sitepages/auxilliarypages/paymentpage/";
})