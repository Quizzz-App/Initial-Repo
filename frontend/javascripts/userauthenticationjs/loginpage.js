
const form = document.querySelector("form");
const toogleresetsection = document.querySelector("#toogleresetsection");
const toogleloginsection = document.querySelector("#toogleloginsection");
const toogleloginsection2 = document.querySelector("#toogleloginsection2");
const resetemailconfirm = document.querySelector("#resetemailconfirm");
 

form.addEventListener("submit",(event)=>{
    event.preventDefault();
});

toogleresetsection.addEventListener("click",()=>{
    form.classList.replace("showlogin","showemailconfirm");
})

toogleloginsection.addEventListener("click",()=>{
   form.classList.replace("showemailconfirm","showlogin");
})

toogleloginsection2.addEventListener("click",()=>{
   form.classList.replace("showresetverify","showlogin");
})

resetemailconfirm.addEventListener("click",()=>{
   form.classList.replace("showemailconfirm","showresetverify");
})

const toggle = document.querySelector(".togglelogin");
const rememberme = document.getElementById("rememberme");

rememberme.addEventListener("click",()=>{
    const classlist=toggle.classList;

    if(Object.values(classlist).includes("active")){
       toggle.classList.remove("active");
    }else{
      toggle.classList.add("active");
    }
})


const showpassword = document.getElementById("showpassword");
const password = document.getElementById("password");

showpassword.addEventListener("click",()=>{
   if(showpassword.innerText=="visibility"){
        showpassword.innerText="visibility_off";
        password.type="password";
   }else{
        showpassword.innerText="visibility";
        password.type="text";
   }
})

