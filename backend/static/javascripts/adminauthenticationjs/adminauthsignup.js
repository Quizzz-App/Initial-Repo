const signUpBtn = document.getElementById("signUpBtn");
const fn = document.querySelector("#fn");
const ln = document.querySelector("#ln");
const un = document.querySelector("#un");
const em = document.querySelector("#em");
const po = document.querySelector(".po");
const pt = document.querySelector(".pt");
const Ustatus = document.querySelector("#status-drop");
const showpassword = document.querySelectorAll(".passwordyard");
const form = document.querySelector("form");

showpassword.forEach((x) => {
  try {
    const show_btn = x.querySelector("#showpassword");
    const hide_btn = x.querySelector("#password");

    show_btn.addEventListener("click", () => {
      if (show_btn.innerText == "visibility") {
        show_btn.innerText = "visibility_off";
        hide_btn.type = "password";
      } else {
        show_btn.innerText = "visibility";
        hide_btn.type = "text";
      }
    });
  } catch (error) {
    
  }
  
});
signUpBtn.addEventListener('click', function(e){
    e.preventDefault();
    e.target.textContent= 'Registering'
    // console.log(fn.value, ln.value, un.value, em.value, po.value, pt.value, Ustatus.value);
    $.ajax({
        type: "POST",
        url: document.getElementById("null").value,
        data: {
          fn: fn.value,
          ln: ln.value,
          un: un.value,
          em: em.value,
          po: po.value,
          pt: pt.value,
          status: Ustatus.value,
          csrfmiddlewaretoken: $("input[name=csrfmiddlewaretoken]").val(),
        },
        success: function (response) {
          if (response.status == "ok") {
            form.classList.replace("showlogin", "showresetverify");
            console.log(response)
          }
        },
        error: function (response) {
          alert("An error occurred");
          console.log(response);
          
        },
      });
})