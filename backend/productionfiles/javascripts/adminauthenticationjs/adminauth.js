
const signInBtn = document.getElementById("toogleresetsection");
const showpassword = document.getElementById("showpassword");
const password = document.getElementById("password");
const username= document.getElementById("username");


showpassword.addEventListener("click", () => {
  if (showpassword.innerText == "visibility") {
    showpassword.innerText = "visibility_off";
    password.type = "password";
  } else {
    showpassword.innerText = "visibility";
    password.type = "text";
  }
});


signInBtn.addEventListener('click',(e)=>{
   e.target.textContent= 'Authenticating';
   $.ajax({
      type: "POST",
      url: `${document.getElementById("null").value}`,
      data: {
        username: username.value,
        password: password.value,
        csrfmiddlewaretoken: $("input[name=csrfmiddlewaretoken]").val(),
      },
      success: function (response) {
         console.log(response)
         if(response.status == 'Success'){
            e.target.textContent= response.msg;
            window.location.href= response.url
         }else{
            alert(response.msg);
            e.target.textContent= 'Retry';
         }
      },
      error: function (response) {
        alert("An error occurred");
      },
    });
});

