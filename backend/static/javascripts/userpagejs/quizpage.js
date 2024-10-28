const courseselect = [...document.getElementsByClassName("courseselect")];
const coursetitle = [...document.getElementsByClassName("coursetitle")];
const quizsettingspopup = document.querySelector(".quizsettingspopup");
const quizsettingspopupclose = document.querySelector("#quizsettingspopupclose");
const quizcourseheading = document.getElementById("quizcourseheading");
const preparenstartquiz = document.getElementById("preparenstartquiz");

courseselect.forEach((coursesel,index)=>{
   coursesel.addEventListener('click',()=>{  
      quizcourseheading.textContent=coursetitle[index].textContent;
      quizsettingspopup.classList.toggle("active",true);
      body.style.overflow="hidden";
   });
});
quizsettingspopupclose.addEventListener('click',()=>{
     quizsettingspopup.classList.toggle("active",false);
     body.style.overflow="auto";
});

preparenstartquiz.addEventListener('click',()=>{
      window.location.href = "./../../auxilliarypages/quizpage/";
});

