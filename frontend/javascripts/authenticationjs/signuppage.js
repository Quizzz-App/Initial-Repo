
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
    window.location.href = "../../sitepages/personalinfopage/";
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