const form = document.querySelector("form");
const regBtn = document.querySelector("#signUpBtn");
const toogleresetsection = document.querySelector("#toogleresetsection");
const toogleloginsection2 = document.querySelector("#toogleloginsection2");

regBtn.addEventListener("click", (event) => {
  event.preventDefault();
  const fn = document.querySelector("#fn");
  const ln = document.querySelector("#ln");
  const un = document.querySelector("#un");
  const em = document.querySelector("#em");
  const po = document.querySelector(".po");
  const pt = document.querySelector(".pt");
  const signupBtn = document.querySelector("#signUpBtn");

  signupBtn.textContent = "Registering...";
  // console.log(fn.value, ln.value, un.value, em.value, po.value, pt.value);

  $.ajax({
    type: "POST",
    url: "/accounts/register/",
    data: {
      fn: fn.value,
      ln: ln.value,
      un: un.value,
      em: em.value,
      po: po.value,
      pt: pt.value,
      csrfmiddlewaretoken: $("input[name=csrfmiddlewaretoken]").val(),
    },
    success: function (response) {
      if (response.status == "ok") {
        form.classList.replace("showlogin", "showresetverify");
      }
    },
    error: function (response) {
      alert("An error occurred");
    },
  });
});

toogleloginsection2.addEventListener("click", () => {
  form.classList.replace("showresetverify", "showlogin");
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

const showpassword = document.querySelectorAll(".passwordyard");
const password = document.getElementById("password");

showpassword.forEach((x) => {
  const show_btn = x.querySelector("#showpassword");
  const hide_btn = x.querySelector("#password");
  console.log(show_btn);

  show_btn.addEventListener("click", () => {
    if (show_btn.innerText == "visibility") {
      show_btn.innerText = "visibility_off";
      hide_btn.type = "password";
    } else {
      show_btn.innerText = "visibility";
      hide_btn.type = "text";
    }
  });
});
