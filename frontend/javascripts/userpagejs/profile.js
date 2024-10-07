
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