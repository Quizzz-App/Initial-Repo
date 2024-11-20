

//Add New Course
const showcourseadd = document.getElementById("showcourseadd");
const showleveladd = document.getElementById("showleveladd");
const courseaddpanel = document.querySelector(".courseaddpanel");
const leveladdpanel = document.querySelector(".leveladdpanel");
const addcoursepanelclose = document.getElementById("addcoursepanelclose");
const addlevelpanelclose = document.getElementById("addlevelpanelclose");

const courseposter = document.getElementById("courseposter");
const addcourseposterbtn = document.getElementById("addcourseposterbtn");
const addcourseposter = document.getElementById("addcourseposter");

// const addsubsgroup = document.getElementById("addsubsgroup");
// const courseaddbtn = document.getElementById("courseaddbtn");

const createCourseBtn = document.getElementById("create-new-course-btn");
const createLevelBtn = document.getElementById("create-new-level-btn");


showcourseadd.addEventListener('click',()=>{
   courseaddpanel.classList.toggle("active",true);
   body.style.overflowY="hidden";
})

showleveladd.addEventListener('click',()=>{
   leveladdpanel.classList.toggle("active",true);
   body.style.overflowY="hidden";
})

addcoursepanelclose.addEventListener('click',()=>{
   courseaddpanel.classList.toggle("active",false);
   body.style.overflowY="auto";
})

addlevelpanelclose.addEventListener('click',()=>{
   leveladdpanel.classList.toggle("active",false);
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
        fetch('/quizz/add-course/', {
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

// Create level
createLevelBtn.addEventListener('click', function(){
   let formData= new FormData();
   const level= document.getElementById("level-title")
   formData.append('question-level', level.value); 
   if (level.value === ''){
       alert('Please enter the level');
   }else{
       fetch('/quizz/add-level/', {
           method: 'POST',
           body: formData
       }).then(response => response.json()
           ).then(response => {
               if (response.status === 'Success'){
                   alert(response.msg);
                  level.value= ''
               //    courseposter.src = ''
                  leveladdpanel.classList.toggle("active",false);
                  body.style.overflowY="auto";    
                  window.location.reload();            
              }else{
                 alert(response.msg);
              }
           })
          .catch(error => {
           console.error(error);
          })
   }
});

// Edit level

const mgLevelContainer= document.getElementById("mg-level");
const mgLevelContainerMain= document.getElementById("mg-level-main");
const showlevelmanageBtn= document.getElementById("showlevelmanage");
const showlevelMainBtns= document.querySelectorAll(".course#level");
const closeBtn= document.querySelector(".closeBtn");
const closeBtn1= document.querySelector(".closeBtn1");
const editbtn= document.getElementById("editleveltitle");
const editlevelconfirm= document.getElementById("editlevelconfirm");
const updtelevelbtn= document.getElementById("updatelevelBtn");

editbtn.addEventListener("click", function(){
   const coursetitlebox= document.getElementById("leveltitlebox")
   coursetitlebox.removeAttribute("disabled");
    coursetitlebox.focus();
    editlevelconfirm.style.display = "flex";
    editbtn.style.display = "none";
})

editlevelconfirm.addEventListener("click", function(){
   const coursetitlebox= document.getElementById("leveltitlebox")
   coursetitlebox.setAttribute("disabled","true");
   editbtn.style.display = "flex";
   editlevelconfirm.style.display = "none";
})

closeBtn.addEventListener("click", function(){
   mgLevelContainer.classList.toggle("active",false);
   body.style.overflowY="auto";
})

closeBtn1.addEventListener("click", function(){
   mgLevelContainerMain.classList.toggle("active",false);
   body.style.overflowY="auto";
})

showlevelmanageBtn.addEventListener("click", function(){
   mgLevelContainer.classList.toggle("active",true);
   body.style.overflowY="hidden";
})

showlevelMainBtns.forEach(x => {
   const btn= x.querySelector("#contbtn #btn-show")
   const data= x.querySelector("#levelData").value
   btn.addEventListener("click", function(){
      updateLevelpanel(data);
   })
})

function updateLevelpanel(levelTitle){
   const old= document.getElementById("old-level");
   old.value= levelTitle;
   const neW= document.getElementById("leveltitlebox");
   neW.value= levelTitle
   mgLevelContainerMain.classList.toggle("active",true);
}

updtelevelbtn.addEventListener("click", function(){
   let formData= new FormData();
   const level= document.getElementById("leveltitlebox")
   formData.append('question-level', level.value);
   formData.append("old", document.getElementById("old-level").value) 
   if (level.value === ''){
       alert('Please enter the level');
   }else{
       fetch('/quizz/update-level/', {
           method: 'POST',
           body: formData
       }).then(response => response.json()
           ).then(response => {
               if (response.status === 'Success'){
                   alert(response.msg);
                  //  level.value= ''
                  // mgLevelContainerMain.classList.toggle("active",false);
                  // body.style.overflowY="auto";    
                  window.location.reload();            
              }else{
                 alert(response.msg);
              }
           })
          .catch(error => {
           console.error(error);
          })
   }
})

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
const course= document.querySelectorAll(".course");
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
// const updatecourseaddbtn = document.getElementById("updatecourseaddbtn");

const updateCourseBtn= document.getElementById("updateCourseBtn");

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

course.forEach((x) => {
   const btn= x.querySelector(".coursecontentupdatebtn")
   btn.addEventListener('click',()=>{
      const coursedata= x.querySelector("#courseData").value.split(',')
      UpdateCoursepanel(coursedata[0], coursedata[1])
   })
})

function UpdateCoursepanel(courseTitle, img){
   const updatetext= courseupdatepanel.querySelector("#coursetitlebox");
   const updateimg= courseupdatepanel.querySelector("#courseupdateposter");
   updatetext.value= courseTitle;
   updateimg.src= img;
   document.querySelector("#old").value= courseTitle
   courseupdatepanel.classList.toggle("active",true);
}

updateCourseBtn.addEventListener("click", function(){
   const updatedTitle= courseupdatepanel.querySelector("#coursetitlebox").value;
   let formData = new FormData();
   formData.append('old', document.getElementById("old").value)
   formData.append("course", updatedTitle);
   if (updateCourseimg != undefined){
      formData.append('img', updateCourseimg);
   }else{
      formData.append('img', '');
   }
   fetch('/quizz/update-course/', {
           method: 'POST',
           body: formData
       }).then(response => response.json()
).then(response => {
    if (response.status === 'Success'){
        alert(response.msg);   
       window.location.reload();            
   }else{
      alert(response.msg);
   }
})
.catch(error => {
console.error(error);
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
// updatecourseaddbtn.addEventListener('click',()=>{
//    const addinp = '<section id="updatesubtopic"><input type="text"><span id="updatecoursesubremovebtn" class="material-symbols-rounded">close</span></section>';
//    const tempNode = document.createElement("div");
//    tempNode.innerHTML = addinp;

//    updatesubsgroup.appendChild(tempNode.firstChild);
//    queryallupdatesubtopicinput();
// })


//Add Question
const showquestionadd = document.getElementById("showquestionadd");
const addquestionpanel = document.querySelector(".addquestionpanel");
const addquestionpanelclose = document.getElementById("addquestionpanelclose");
const addquestionBtn = document.querySelector(".answersubmit > button");

showquestionadd.addEventListener('click',()=>{
   addquestionpanel.classList.toggle("active",true);
   body.style.overflowY="hidden";
})
addquestionpanelclose.addEventListener('click',()=>{
   addquestionpanel.classList.toggle("active",false);
   body.style.overflowY="auto";
})

addquestionBtn.addEventListener("click", function(e){
   const course= document.getElementById("course-select").value;
   const level= document.getElementById("level-select").value;
   const question= document.getElementById("question").value;
   const correctAns= document.getElementById("correct-ans").value;
   const incorrectAns= document.querySelectorAll("#incorrect-ans");

   const checkList= [course, level, question, correctAns, incorrectAns];
   let allValid= true;
   for(var x=0; x <= checkList.length; x++){
      if(x == 4){
         checkList[x].forEach((value) => {
            value.value == ''?allValid=false:''
         })
      }else{
         checkList[x] == ''?allValid=false:''
      }
      if(!allValid){
         break;
      }
   }
   !allValid?alert("Please make sure to complete the question"):''
   if(allValid){
      let incorrects= '';
      incorrectAns.forEach((element, index) => {
         index != 2?incorrects+= `${element.value},`:incorrects+= element.value
      })
      let formData= new FormData();
      formData.append('question', question);
      formData.append('correct-ans', correctAns);
      formData.append('incorrect-ans', incorrects);
      formData.append('category', course);
      formData.append('level', level);
      e.target.textContent= 'Uploading question....'
      fetch('/quizz/add-questions/', {
         method: 'POST',
         body: formData
      }).then(response => response.json())
      .then(response => {
         if (response.status === 'Success'){
             alert(response.msg);
         addquestionpanel.classList.toggle("active",false);
            body.style.overflowY="auto";    
            window.location.reload();            
        }else{
           alert(response.msg);
           e.target.textContent= 'Upload Question';
        }
     })
    .catch(error => {
     console.error(error);
    })
   }
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

const updateQBtn= document.querySelector('#btnSub');

showquestionmanage.addEventListener('click',()=>{
   managequestionpanel.classList.toggle("active",true);
   body.style.overflowY="hidden";
})
managequestionpanelclose.addEventListener('click',()=>{
   managequestionpanel.classList.toggle("active",false);
   body.style.overflowY="auto";
})

questeditholderclose.addEventListener('click',()=>{
   questeditpanel.classList.toggle("active",false);
})


questdeleteconfirm.addEventListener('click',()=>{
   questdeletepanel.classList.toggle("active",false);
})
questdeletecancel.addEventListener('click',()=>{
   questdeletepanel.classList.toggle("active",false);
})

const questionSect= document.querySelectorAll(".quest");

questionSect.forEach(x => {
   const btnEdit= x.querySelector('#questeditbtn');
   const btnDelete= x.querySelector("#questdeletebtn")
   const uID= x.querySelector("#uid").value;

   btnEdit.addEventListener("click", function(){
   fetch(`/quizz/get-question/${uID}/`)
   .then(response => response.json())
   .then(response => {updateQuestionPanel(response)})
   .catch(error => {
      alert("Something went wrong try again")
     console.error(error);
   })
   })
   
   btnDelete.addEventListener("click", function(){
      questdeletepanel.classList.toggle("active",true);
   })
})

function updateQuestionPanel(data){
   document.getElementById("editTTA").value=data.question;
   document.getElementById("editUID").value= data.id
   document.getElementById("editCorrectA").value=data.answer;
   const inc= document.querySelectorAll("#editINCorrectA");
   const incA= data.incorrect.split(',')
   inc.forEach((element, index) => {
      element.value= incA[index]
   })
   questeditpanel.classList.toggle("active",true);

}

updateQBtn.addEventListener("click", function(e){
   const uID= document.getElementById("editUID").value;
   const question= document.getElementById("editTTA").value;
   const correctAns= document.getElementById("editCorrectA").value;
   const incorrectAns= document.querySelectorAll("#editINCorrectA");
   const checkList= [question, correctAns, incorrectAns];
   let allValid= true;
   for(var x=0; x <= checkList.length; x++){
      if(x == 2){
         checkList[x].forEach((value) => {
            value.value == ''?allValid=false:''
         })
      }else{
         checkList[x] == ''?allValid=false:''
      }
      if(!allValid){
         break;
      }  
   }
   !allValid?alert("Please make sure to complete the question"):''
   if(allValid){
      let incorrects= '';
      incorrectAns.forEach((element, index) => {
         index!= 2?incorrects+= `${element.value},`:incorrects+= element.value
      })
      let formData= new FormData();
      formData.append('question', question);
      formData.append('correct-ans', correctAns);
      formData.append('incorrect-ans', incorrects);
      formData.append('id', uID);
      e.target.textContent= 'Updating question....'
      fetch('/quizz/update-question/', {
         method: 'POST',
         body: formData
      }).then(response => response.json())
     .then(response => {
       if (response.status === 'Success'){
           alert(response.msg);
           questeditpanel.classList.toggle("active",false);
           body.style.overflowY="auto";    
           window.location.reload();            
       }else{
          alert(response.msg);
          e.target.textContent= 'Update Question';
       }
     })
     .catch(error => {
       console.error(error);
      })
   }
})

const ansC = document.querySelectorAll("#answeredititem");
const queC = document.querySelector("#questedit");

ansC.forEach(x=>{
   const coursetitlebox= x.querySelector("textarea");
   const editcoursetitlebtn= x.querySelector("#edit");
   const editcourseconfirmbtn= x.querySelector("#check");

   editcoursetitlebtn.addEventListener('click',()=>{
      coursetitlebox.removeAttribute("disabled");
      coursetitlebox.focus();
      editcourseconfirmbtn.style.display = "flex";
      editcoursetitlebtn.style.display = "none";
  })
  editcourseconfirmbtn.addEventListener('click',()=>{
      coursetitlebox.setAttribute("disabled",true);
      editcoursetitlebtn.style.display = "flex";
      editcourseconfirmbtn.style.display = "none";
  })
})