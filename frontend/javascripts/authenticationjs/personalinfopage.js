
const form = document.querySelector("form");
const toogleresetsection = document.querySelector("#toogleresetsection");

form.addEventListener("submit",(event)=>{
   event.preventDefault();
});

toogleresetsection.addEventListener("click",()=>{
   window.location.href = "../../sitepages/userpages/dashboard/";
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