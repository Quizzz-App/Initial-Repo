const form = document.querySelector("form");
const toogleresetsection = document.querySelector("#toogleresetsection");
const toogleloginsection = document.querySelector("#toogleloginsection");
const toogleloginsection2 = document.querySelector("#toogleloginsection2");
const resetemailconfirm = document.querySelector("#resetemailconfirm");
const logBtn = document.querySelector("#loginuser");
const resetEl = document.querySelector("#ps-reset");
try {
  const msg= document.querySelector('.message')
  if(msg.classList.contains('error')){
    alertPopup(alert[1], msg.textContent)
  }else if(msg.classList.contains('success')){
    alertPopup(alert[0], msg.textContent)
  }
} catch (error) {
}

logBtn.addEventListener("click", (event) => {
  event.preventDefault();
  const un = document.querySelector(".un");
  const ps = document.querySelector(".ps");

  event.target.textContent = "Authenticating...";
  // console.log(fn.value, ln.value, un.value, em.value, po.value, pt.value);

  $.ajax({
    type: "POST",
    url: "/accounts/sign-in/",
    data: {
      un: un.value,
      ps: ps.value,
      csrfmiddlewaretoken: $("input[name=csrfmiddlewaretoken]").val(),
    },
    success: function (response) {
      console.log(response)
      if (response.code == 200 && response.state == 'Success') {
        alertPopup(alert[0], 'You have logged in successfully')
        window.location.href = `/accounts/user/${response.un}/dashboard/`;
      }else if(response.code == 400 && response.state == 'activation'){
        alertPopup(alert[1], response.msg)
        event.target.textContent = 'Activation Required'
      }else{
        alertPopup(alert[1], response.msg)
        event.target.textContent= 'Retry'
      }
    },
    error: function (response) {
      alertPopup(alert[1], "An error occurred");
    },
  });
});

toogleresetsection.addEventListener("click", () => {
  form.classList.replace("showlogin", "showemailconfirm");
});

toogleloginsection.addEventListener("click", () => {
  form.classList.replace("showemailconfirm", "showlogin");
});

toogleloginsection2.addEventListener("click", () => {
  form.classList.replace("showresetverify", "showlogin");
});

resetemailconfirm.addEventListener("click", (e) => {
  if (resetEl.value !== ''){
    e.target.textContent= 'Sending Reset Link..'
    $.ajax({
      type: "POST",
      url: "/accounts/password-reset/request/",
      data: {
        email: resetEl.value,
        csrfmiddlewaretoken: $("input[name=csrfmiddlewaretoken]").val(),
      },
      success: function (response) {
        if (response.code == 200){
          form.classList.replace("showemailconfirm", "showresetverify");
          alertPopup(alert[0], response.msg)
        }else{
          alertPopup(alert[1], response.msg)
          e.target.textContent= 'Confirm Email'
        }
      },
      error: function (response) {
        alertPopup(alert[1], "An error occurred")
      },
    });
  }else{
    e.target.textContent= 'Confirm Email'
    alertPopup(alert[1], "Please enter your email")
  }
});

const toggle = document.querySelector(".togglelogin");
const rememberme = document.getElementById("rememberme");

rememberme.addEventListener("click", () => {
  const classlist = toggle.classList;

  if (Object.values(classlist).includes("active")) {
    toggle.classList.remove("active");
  } else {
    toggle.classList.add("active");
  }
});

const showpassword = document.getElementById("showpassword");
const password = document.getElementById("password");

showpassword.addEventListener("click", () => {
  if (showpassword.innerText == "visibility") {
    showpassword.innerText = "visibility_off";
    password.type = "password";
  } else {
    showpassword.innerText = "visibility";
    password.type = "text";
  }
});
