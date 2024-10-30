const form = document.querySelector("form");
const toogleresetsection = document.querySelector("#toogleresetsection");
const toogleloginsection = document.querySelector("#toogleloginsection");
const toogleloginsection2 = document.querySelector("#toogleloginsection2");
const resetemailconfirm = document.querySelector("#resetemailconfirm");
const logBtn = document.querySelector("#loginuser");

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
      if (response.status == "ok") {
        event.target.textContent = "Authenticated";
        window.location.href = `/accounts/user/${response.un}/dashboard/`;
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

resetemailconfirm.addEventListener("click", () => {
  form.classList.replace("showemailconfirm", "showresetverify");
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
