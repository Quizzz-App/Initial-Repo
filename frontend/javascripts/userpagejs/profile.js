
const changeprofileimagebtn = document.getElementById("changeprofileimagebtn");
const profileimage = document.getElementById("profileimage");
const changeprofileimage = document.getElementById("changeprofileimage");

changeprofileimagebtn.addEventListener('click',()=>{
   changeprofileimage.click();
});

changeprofileimage.addEventListener('change',(event)=>{
   var imgfile = event.target.files[0];
  
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