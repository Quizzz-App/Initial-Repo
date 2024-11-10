
const changeprofileimagebtn = document.getElementById("changeprofileimagebtn");
const profileimage = document.getElementById("profileimage");
const changeprofileimage = document.getElementById("changeprofileimage");
const profileUpdateBtn = document.getElementById("btn-update-profile");
const passwordUpdateBtn = document.getElementById("btn-update-pass");

var imgfile= '';
changeprofileimagebtn.addEventListener('click',()=>{
   changeprofileimage.click();
});

changeprofileimage.addEventListener('change',(event)=>{
    imgfile = event.target.files[0];
  
   if (imgfile) { 
      const reader = new FileReader();
      reader.readAsDataURL(imgfile);
      reader.onload = function(e) {
         profileimage.src = e.target.result;
      }  
   }

});

const passinput = [...document.getElementsByClassName("passinput")];
const visiblebtn = [...document.querySelectorAll("#visiblebtn")];

visiblebtn.forEach((visbtn,index)=>{
      visbtn.addEventListener('click',()=>{
         if(visbtn.innerText=="visibility"){
            visbtn.innerText="visibility_off";
            passinput[index].type="password";
        }else{
            visbtn.innerText="visibility";
            passinput[index].type="text";
         }
      });
});

profileUpdateBtn.addEventListener('click', function(e){
   e.target.textContent= 'Updating Profile'
   const fn= document.getElementById("fn");
   const ln= document.getElementById("ln");
   const email= document.getElementById("email");
   // const ph;
   const ps= document.getElementById("ps");

   let formData= new FormData();
   formData.append("fn", fn.value)
   formData.append("ln", ln.value)
   formData.append("email", email.value)
   formData.append("ps", ps.value)
   formData.append('img', imgfile)


   fetch('/accounts/user/update/profile/',{
      method: 'POST',
      body: formData
   }).then(response => response.json())
   .then(response => {
      e.target.textContent= 'Save Profile Changes'
         alert(response.msg);
         if (response.state === 'Success'){
            window.location.href= `/accounts/user/${response.user}/update-profile/`
         }
   })
   .catch(err => {
      e.target.textContent= 'Save Profile Changes'
      alert("An error occurred");
   })
})

passwordUpdateBtn.addEventListener('click', function(e){
   e.target.textContent= 'Updating Password'
   const old_password= document.getElementById("oldP");
   const newP= document.getElementById("p1");
   const confP= document.getElementById("p2");

   $.ajax({
      type: "POST",
      url: `/accounts/user/update/password/`,
      data: {
         oldP: old_password.value,
         np: newP.value,
         cp: confP.value,
      },
      success: function (response) {
         e.target.textContent= 'Save Password Changes'
         alert(response.msg);
         if (response.state === 'Success'){
            window.location.href= `/accounts/user/${response.user}/update-profile/`
         }
      },
      error: function (response) {
         e.target.textContent= 'Save Password Changes'
        alert("An error occurred");
      },
    }); 
})
