const confirmBtn= document.getElementById("confirmPayment");
const cancelBtn= document.getElementById("cancelPayment");
const verifyPopup = document.querySelector(".quizsettingspopup");
const verifypopupclose = document.querySelector("#quizsettingspopupclose");
const verifyBtn= document.getElementById("verifyBtn");

var user;

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
           verifyPopup.classList.toggle("active",true);
           document.getElementById('msg').textContent= data.message
           document.getElementById('ref').value= data.data.reference
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