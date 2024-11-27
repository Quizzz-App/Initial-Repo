const form = document.querySelector("form");
const toogleresetsection = document.querySelector("#toogleresetsection");
const toogleloginsection = document.querySelector("#toogleloginsection");
const toogleloginsection2 = document.querySelector("#toogleloginsection2");
const resetemailconfirm = document.querySelector("#resetemailconfirm");
const logBtn = document.querySelector("#loginuser");
const resetEl = document.querySelector("#ps-reset");


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
      if (response.status == 200 && response.state == 'Success') {
        event.target.textContent = "Authenticated";
        window.location.href = `/accounts/user/${response.un}/dashboard/`;
      }else if(response.status == 200 && response.state == 'activation'){
        alert(response.msg)
        event.target.textContent = 'Activation Required'
      }else{
        alert(response.msg)
        event.target.textContent= 'Retry'
      }
    },
    error: function (response) {
      alert("An error occurred");
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
  e.target.textContent= 'Sending Reset Link..'
  $.ajax({
    type: "POST",
    url: "/accounts/password-reset/request/",
    data: {
      email: resetEl.value,
      csrfmiddlewaretoken: $("input[name=csrfmiddlewaretoken]").val(),
    },
    success: function (response) {
      form.classList.replace("showemailconfirm", "showresetverify");
    },
    error: function (response) {
      alert("An error occurred");
    },
  });
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
