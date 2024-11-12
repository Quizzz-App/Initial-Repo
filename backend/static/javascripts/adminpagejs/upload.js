

//Add New Course
const showcourseadd = document.getElementById("showcourseadd");
const courseaddpanel = document.querySelector(".courseaddpanel");
const addcoursepanelclose = document.getElementById("addcoursepanelclose");

const courseposter = document.getElementById("courseposter");
const addcourseposterbtn = document.getElementById("addcourseposterbtn");
const addcourseposter = document.getElementById("addcourseposter");

// const addsubsgroup = document.getElementById("addsubsgroup");
// const courseaddbtn = document.getElementById("courseaddbtn");

const createCourseBtn = document.getElementById("create-new-course-btn");


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
   uploadCourseimg = event.target.files[0];
  
   if (uploadCourseimg) { 
      const reader = new FileReader();
      reader.readAsDataURL(uploadCourseimg);
      reader.onload = function(e) {
         courseposter.src = e.target.result;
      }  
   }
});

createCourseBtn.addEventListener('click', function(){
    let formData= new FormData();
    const course= document.getElementById("cat-title")
    formData.append('question-category', course.value); 
    if (uploadCourseimg === undefined){
        alert('Please select an image for the course');
    }else{
        formData.append('img', uploadCourseimg)
        fetch('/quizz/course-management/', {
            method: 'POST',
            body: formData
        }).then(response => response.json()
            ).then(response => {
                if (response.status === 'Success'){
                    alert(response.msg);
                   course.value= ''
                //    courseposter.src = ''
                   courseaddpanel.classList.toggle("active",false);
                   body.style.overflowY="auto";                
               }else{
                  alert(response.msg);
               }
            })
           .catch(error => {
            console.error(error);
           })
    }
});

// function queryalladdsubtopicinput(){
//    const subtopicinputs = [...document.querySelectorAll("#addsubtopic")];
//    const subremovebtns = [...document.querySelectorAll("#coursesubremovebtn")];

//    subremovebtns.forEach((removebtn,i) => {
//       removebtn.addEventListener('click',()=>{
//          addsubsgroup.removeChild(subtopicinputs[i]);
//       })
//    });
// }
// courseaddbtn.addEventListener('click',()=>{
//    const addinp = '<section id="addsubtopic"><input type="text"><span id="coursesubremovebtn" class="material-symbols-rounded">close</span></section>';
//    const tempNode = document.createElement("div");
//    tempNode.innerHTML = addinp;

//    addsubsgroup.appendChild(tempNode.firstChild);
//    queryalladdsubtopicinput();
// })


//Manage Course
const showcoursemanage = document.getElementById("showcoursemanage");
const coursemanagepanel = document.querySelector(".coursemanagepanel");
const managecoursepanelclose = document.getElementById("managecoursepanelclose");

const coursecontentupdatebtn = [...document.querySelectorAll(".coursecontentupdatebtn")];
const courseupdatepanel = document.querySelector(".courseupdatepanel");
const courseupdateholderclose = document.getElementById("updateholderclose");

const coursetitlebox = document.getElementById("coursetitlebox");
const editcoursetitlebtn = document.getElementById("editcoursetitle");
const editcourseconfirmbtn = document.getElementById("editcourseconfirm");

const courseupdateposter = document.getElementById("courseupdateposter");
const courseupdateposterbtn = document.getElementById("courseupdateposterbtn");
const updatecourseposter = document.getElementById("updatecourseposter");

const subcoursetitlebox = [...document.getElementsByClassName("subcoursetitlebox")];
const subcoursetitleedit = [...document.querySelectorAll("#subcoursetitleedit")];
const subcoursetitleconfirm = [...document.querySelectorAll("#subcoursetitleconfirm")];
const subcoursetitledelete = [...document.querySelectorAll("#subcoursetitledelete")];

const subdeletepanel = document.querySelector(".subdeletepanel");
const subdeleteconfirm = document.getElementById("subdeleteconfirm");
const subdeletecancel = document.getElementById("subdeletecancel");


const updatesubsgroup = document.getElementById("updatesubsgroup");
const updatecourseaddbtn = document.getElementById("updatecourseaddbtn");

var uploadCourseimg;
var updateCourseimg;

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


editcoursetitlebtn.addEventListener('click',()=>{
    coursetitlebox.removeAttribute("disabled");
    coursetitlebox.focus();
    editcourseconfirmbtn.style.display = "flex";
    editcoursetitlebtn.style.display = "none";
})
editcourseconfirmbtn.addEventListener('click',()=>{
    coursetitlebox.setAttribute("disabled","true");
    editcoursetitlebtn.style.display = "flex";
    editcourseconfirmbtn.style.display = "none";
})


courseupdateposterbtn.addEventListener('click',()=>{
   updatecourseposter.click();
});
updatecourseposter.addEventListener('change',(event)=>{
   updateCourseimg = event.target.files[0];
  
   if (updateCourseimg) { 
      const reader = new FileReader();
      reader.readAsDataURL(updateCourseimg);
      reader.onload = function(e) {
         courseupdateposter.src = e.target.result;
      }  
   }
});


subcoursetitleedit.forEach((subcoursetitle,i)=>{
    subcoursetitle.addEventListener('click',()=>{
      subcoursetitlebox[i].removeAttribute("disabled");
      subcoursetitlebox[i].focus();
      subcoursetitleconfirm[i].style.display = "flex";
      subcoursetitle.style.display = "none";
    })
})
subcoursetitleconfirm.forEach((subcourseconfirm,i)=>{
   subcourseconfirm.addEventListener('click',()=>{
     subcoursetitlebox[i].setAttribute("disabled",true);
     subcoursetitleedit[i].style.display = "flex";
     subcourseconfirm.style.display = "none";
   })
})
subcoursetitledelete.forEach((subcoursedelete,i)=>{
   subcoursedelete.addEventListener('click',()=>{
      subdeletepanel.classList.toggle("active",true);
   })
})
subdeleteconfirm.addEventListener('click',()=>{
   subdeletepanel.classList.toggle("active",false);
})
subdeletecancel.addEventListener('click',()=>{
   subdeletepanel.classList.toggle("active",false);
})



function queryallupdatesubtopicinput(){
   const subtopicinputs = [...document.querySelectorAll("#updatesubtopic")];
   const subremovebtns = [...document.querySelectorAll("#updatecoursesubremovebtn")];

   subremovebtns.forEach((removebtn,i) => {
      removebtn.addEventListener('click',()=>{  
         updatesubsgroup.removeChild(subtopicinputs[i]);
      })
   });
}
updatecourseaddbtn.addEventListener('click',()=>{
   const addinp = '<section id="updatesubtopic"><input type="text"><span id="updatecoursesubremovebtn" class="material-symbols-rounded">close</span></section>';
   const tempNode = document.createElement("div");
   tempNode.innerHTML = addinp;

   updatesubsgroup.appendChild(tempNode.firstChild);
   queryallupdatesubtopicinput();
})


//Add Question
const showquestionadd = document.getElementById("showquestionadd");
const addquestionpanel = document.querySelector(".addquestionpanel");
const addquestionpanelclose = document.getElementById("addquestionpanelclose");


showquestionadd.addEventListener('click',()=>{
   addquestionpanel.classList.toggle("active",true);
   body.style.overflowY="hidden";
})
addquestionpanelclose.addEventListener('click',()=>{
   addquestionpanel.classList.toggle("active",false);
   body.style.overflowY="auto";
})


//Manage Question
const showquestionmanage = document.getElementById("showquestionmanage");
const managequestionpanel = document.querySelector(".managequestionpanel");
const managequestionpanelclose = document.getElementById("managequestionpanelclose");

const questeditbtn = [...document.querySelectorAll("#questeditbtn")];
const questeditpanel = document.querySelector(".questeditpanel");
const questeditholderclose = document.getElementById("questeditholderclose");

const questdeletebtn = [...document.querySelectorAll("#questdeletebtn")];
const questdeletepanel = document.querySelector(".questdeletepanel");
const questdeleteconfirm = document.getElementById("questdeleteconfirm");
const questdeletecancel = document.getElementById("questdeletecancel");

showquestionmanage.addEventListener('click',()=>{
   managequestionpanel.classList.toggle("active",true);
   body.style.overflowY="hidden";
})
managequestionpanelclose.addEventListener('click',()=>{
   managequestionpanel.classList.toggle("active",false);
   body.style.overflowY="auto";
})


questeditbtn.forEach((editbtn,i)=>{
   editbtn.addEventListener('click',()=>{
      questeditpanel.classList.toggle("active",true);
   })
})
questeditholderclose.addEventListener('click',()=>{
   questeditpanel.classList.toggle("active",false);
})


questdeletebtn.forEach((deletebtn,i)=>{
   deletebtn.addEventListener('click',()=>{
      questdeletepanel.classList.toggle("active",true);
   })
})
questdeleteconfirm.addEventListener('click',()=>{
   questdeletepanel.classList.toggle("active",false);
})
questdeletecancel.addEventListener('click',()=>{
   questdeletepanel.classList.toggle("active",false);
})