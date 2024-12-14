const showpasswordEl= document.querySelectorAll('.passwordyard');
const btnReset= document.querySelector("#loginuser")



showpasswordEl.forEach(x =>{
    const showpassword= x.querySelector('#showpassword');
    const password= x.querySelector("#password");
    showpassword.addEventListener("click", () => {
        if (showpassword.innerText == "visibility") {
          showpassword.innerText = "visibility_off";
          password.type = "password";
        } else {
          showpassword.innerText = "visibility";
          password.type = "text";
        }
      });
})

btnReset.addEventListener('click', function(){
    const passwords= document.querySelectorAll('#password');
    if(passwords[0].value && passwords[1].value && passwords[0].value == passwords[1].value){
        
        $.ajax({
            type: "POST",
            url: `/accounts/password-change/${document.getElementById("null").value}/`,
            data: {
              ps1: passwords[0].value,
              csrfmiddlewaretoken: $("input[name=csrfmiddlewaretoken]").val(),
            },
            success: function (response) {
              if(response.code == 200){
                window.location.href= `/accounts/sign-in/`
              }else{
                alertPopup(alert[1], response.msg)
              }
            },
            error: function (response) {
              alert("An error occurred");
            },
          });
    }else if (passwords[0].value !== passwords[1].value){
        alert('Make sure both passwords match');
    }else{
        alert('You failed to input password');
    }
})