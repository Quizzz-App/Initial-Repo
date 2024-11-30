const confirmBtn= document.getElementById("confirmPayment");
const cancelBtn= document.getElementById("cancelPayment");
const verifyPopup = document.querySelector(".quizsettingspopup");
const verifypopupclose = document.querySelector("#quizsettingspopupclose");
const verifyBtn= document.getElementById("verifyBtn");

var user;
function getVoucher(refCode, msg) {  
  let userInput;  
  let formData= new FormData();

  formData.append("ref_code", refCode)

  do {  
      userInput = prompt(msg);  
      if (!userInput || userInput.trim() === "") {  
          alertPopup(alert[1],"You didn't input anything. Please try again.");  
      }  
  } while (!userInput || userInput.trim() === ""); 
  formData.append("opt_code", userInput);
  fetch('/payment/first-Momo-Transaction/submit-otp/', {
    method: 'POST',
    body: formData,
  }).then(response => response.json())
  .then(response => {
    console.log(response)
    if(response.status == 'false'){
      alertPopup(alert[1], response.message); 
      getVoucher(refCode, response.message)
    }else if (response.status == 'true'){
      verifyPopup.classList.toggle("active",true);
      document.getElementById('msg').textContent= response.message
      document.getElementById('ref').value= response.data.reference
    }
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
          e.target.textContent= 'Confirm and Process Payment'
           console.log(data)
           if (data.data.status == "send_otp"){
            getVoucher(data.data.reference, `${data.data.display_text} in the prompt above`)
           }else if (data.data.status == "pay_offline"){
             verifyPopup.classList.toggle("active",true);
             document.getElementById('msg').textContent= data.data.display_text
             document.getElementById('ref').value= data.data.reference
           }else if (data.data.status == 'failed'){
            alertPopup(alert[1],"Transaction failed try again"); 
          }
        },
        error: function (xhr, status, error) {
          console.error("Error:", error);
          e.target.textContent= 'Confirm and Process Payment'
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
      console.log(data)
      if(data.api.data.status === 'success'){
        document.getElementById('msg').textContent= data.api.message
        document.getElementById('verifyBtn').style.display= 'none'
        verifypopupclose.style.display= 'block';
        user= data.user;
      }else if (data.api.data.status === "failed"){
        alertPopup(alert[1],`Transaction failed try again\nERROR:${data.api.data.message}`); 
        verifyPopup.classList.toggle("active",false);
      }else if (data.api.data.status === "ongoing"){
        alertPopup(alert[1],`Transaction failed try again\nERROR:${data.api.data.gateway_response}`); 
        verifyPopup.classList.toggle("active",false);
      }
    },
    error: function (xhr, status, error) {
      console.error("Error:", error);
      alertPopup(alert[1],error);
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