
//Add New Course
const showcourseadd = document.getElementById("showcourseadd");
const courseaddpanel = document.querySelector(".courseaddpanel");
const addcoursepanelclose = document.getElementById("addcoursepanelclose");
const courseposter = document.getElementById("courseposter");
const addcourseposterbtn = document.getElementById("addcourseposterbtn");
const addcourseposter = document.getElementById("addcourseposter");
const addsubsgroup = document.getElementById("addsubsgroup");
const courseaddbtn = document.getElementById("courseaddbtn");

const subtopicinput = addsubsgroup.cloneNode(true);

showcourseadd.addEventListener('click',()=>{
   courseaddpanel.classList.toggle("active",true);
   body.style.overflowY="hidden";
})
addcoursepanelclose.addEventListener('click',()=>{
   courseaddpanel.classList.toggle("active",false);
   body.style.overflowY="auto";
})

addcourseposterbtn.addEventListener('click',()=>{
   addcourseposter.click();
});
addcourseposter.addEventListener('change',(event)=>{
   var imgfile = event.target.files[0];
  
   if (imgfile) { 
      const reader = new FileReader();
      reader.readAsDataURL(imgfile);
      reader.onload = function(e) {
         courseposter.src = e.target.result;
      }  
   }
});
function queryallsubtopicinput(){
   const addsubtopicinputs = [...document.querySelectorAll("#addsubtopic")];
   const coursesubremovebtns = [...document.querySelectorAll("#coursesubremovebtn")];

   coursesubremovebtns.forEach((coursesubremovebtn,i) => {
      coursesubremovebtn.addEventListener('click',()=>{
         const childcount = addsubsgroup.childElementCount;
         
         if(childcount>1){
            addsubsgroup.removeChild(addsubtopicinputs[i]);
          }
      })
   });
  
}
courseaddbtn.addEventListener('click',()=>{
   addsubsgroup.innerHTML += subtopicinput.innerHTML;
   queryallsubtopicinput();
})


//Manage Course
const showcoursemanage = document.getElementById("showcoursemanage");
const coursemanagepanel = document.querySelector(".coursemanagepanel");
const managecoursepanelclose = document.getElementById("managecoursepanelclose");

const coursecontentupdatebtn = [...document.querySelectorAll(".coursecontentupdatebtn")];
const courseupdatepanel = document.querySelector(".courseupdatepanel");
const courseupdateholderclose = document.getElementById("updateholderclose");

showcoursemanage.addEventListener('click',()=>{
   coursemanagepanel.classList.toggle("active",true);
   body.style.overflowY="hidden";
})
managecoursepanelclose.addEventListener('click',()=>{
   coursemanagepanel.classList.toggle("active",false);
   body.style.overflowY="auto";
})

coursecontentupdatebtn.forEach((coursecontentupdate)=>{
    coursecontentupdate.addEventListener('click',()=>{
         courseupdatepanel.classList.toggle("active",true);
    })
})
courseupdateholderclose.addEventListener('click',()=>{
   courseupdatepanel.classList.toggle("active",false);
})