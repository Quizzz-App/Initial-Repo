
const progressRing = document.querySelector('.progress-ring circle');
const timericon =  document.getElementById("timericon");
const progressText = document.getElementById('progress-text');

var progressstart=0;
var currentprogress=0;
var calctime=1*40;

function updateProgress() {
   currentprogress=((progressstart/calctime)*100);
 
  progressText.textContent = `${convertSecondsToTime(progressstart)}`;
  progressRing.style.strokeDashoffset = 0 + ((currentprogress/100) * 628.32);
   
  progressstart++;
  
  if (progressstart <= calctime) {
    setTimeout(updateProgress, 1000);
  }else{
     progressRing.style.fill = "var(--primitivecolor)";
     progressText.textContent = "Time Up";
     timericon.style.color = "var(--primarycolor)";
     progressText.style.color = "var(--primarycolor)";
  }

}

updateProgress();

function convertSecondsToTime(seconds) {
   let minutes = Math.floor((seconds % 3600) / 60);
   let secs = seconds % 60;

   // Pad the hours, minutes, and seconds with leading zeros if needed
   minutes = String(minutes).padStart(2, '0');
   secs = String(secs).padStart(2, '0');

   return `${minutes}:${secs}`;
}


const answeroption = [...document.getElementsByClassName("option")];

answeroption.forEach((option)=>{
      option.addEventListener('click',()=>{
          for(var i=0;i<answeroption.length;i++){
             answeroption[i].classList.toggle("active",false);
          }
          option.classList.toggle("active",true);
      });
});

/* Result Pop Panel */
const resultpopbutton = document.getElementById("resultpopbtn");
const resultdisplaypanel = document.querySelector(".resultdisplaypanel");
const quizretakebtn = document.getElementById("quizretakebtn");
const quizpageredirectbtn = document.getElementById("quizpageredirectbtn");

resultpopbutton.addEventListener('click',()=>{
   resultdisplaypanel.classList.toggle("active",true);
   body.style.overflow = "hidden";
});
quizretakebtn.addEventListener('click',()=>{
   resultdisplaypanel.classList.toggle("active",false);
   body.style.overflow = "auto";
});
quizpageredirectbtn.addEventListener('click',()=>{
   window.location.href = "/sitepages/userpages/quizpage/";
});
