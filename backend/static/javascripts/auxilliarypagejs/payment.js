const confirmBtn= document.getElementById("confirmPayment");
const cancelBtn= document.getElementById("cancelPayment");
const verifyPopup = document.querySelector(".quizsettingspopup");
const verifypopupclose = document.querySelector("#quizsettingspopupclose");
const verifyBtn= document.getElementById("verifyBtn");

var user;
function getVoucher(refCode) {  
  let userInput;  
  let formData= new FormData();

  formData.append("ref_code", refCode)

  do {  
      userInput = prompt("Please enter your generated voucher");  
      if (!userInput || userInput.trim() === "") {  
          alert("You didn't input anything. Please try again.");  
      }  
  } while (!userInput || userInput.trim() === ""); 
  formData.append("opt_code", userInput);
  fetch('/payment/first-Momo-Transaction/submit-otp/', {
    method: 'POST',
    body: formData,
  }).then(response => response.json())
  .then(response => {
    verifyPopup.classList.toggle("active",true);
    document.getElementById('msg').textContent= response.message
    document.getElementById('ref').value= response.data.reference
  })
  .catch(err => console.error)
}  


confirmBtn.addEventListener('click', function(e){
  e.target.textContent= 'Intiating Transaction'
    $.ajax({
        type: "POST",
        url: "/payment/intiate-Momo-transaction/",
        data: JSON.stringify(''),
        contentType: "application/json; charset=utf-8",
        dataType: "json",
        success: function(data){
           console.log(data)
           if (data.data.status == "send_otp"){
            alertPopup(alert[2],`${data.data.display_text} in the prompt above`)
            getVoucher(data.data.reference)
           }else{
             verifyPopup.classList.toggle("active",true);
             document.getElementById('msg').textContent= data.message
             document.getElementById('ref').value= data.data.reference
           }
        },
        error: function (xhr, status, error) {
          console.error("Error:", error);
        },
      });
})

verifyBtn.addEventListener('click', function verifyTransaction(e){
  e.target.textContent= 'Verifying Transaction'
  $.ajax({
    type: "GET",
    url: `/payment/verifyDeposite/${document.getElementById('ref').value}/`,
    data: JSON.stringify(''),
    contentType: "application/json; charset=utf-8",
    dataType: "json",
    success: function(data){
       document.getElementById('msg').textContent= data.api.message
       document.getElementById('verifyBtn').style.display= 'none'
       user= data.user;
       
    },
    error: function (xhr, status, error) {
      console.error("Error:", error);
      alert(error);
    },
  });
})

verifypopupclose.addEventListener('click',()=>{
  verifyPopup.classList.toggle("active",false);
  window.location.href=`/accounts/user/${user}/wallet/`
});

cancelBtn.addEventListener('click', function(){
  $.ajax({
    type: "DELETE",
    url: "/payment/intiate-Momo-transaction/",
    data: JSON.stringify(''),
    contentType: "application/json; charset=utf-8",
    dataType: "json",
    success: function(data){
       window.location.href= `/accounts/user/${data.user}/wallet/`
    },
    error: function (xhr, status, error) {
      
    },
  });
})