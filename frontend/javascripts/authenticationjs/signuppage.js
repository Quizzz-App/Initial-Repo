
const form = document.querySelector("form");
const toogleresetsection = document.querySelector("#toogleresetsection");
const toogleloginsection2 = document.querySelector("#toogleloginsection2");

form.addEventListener("submit",(event)=>{
   event.preventDefault();
});

toogleresetsection.addEventListener("click",()=>{
   form.classList.replace("showlogin","showresetverify");
})

toogleloginsection2.addEventListener("click",()=>{
   form.classList.replace("showresetverify","showlogin");
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