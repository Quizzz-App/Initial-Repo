const dataInput = document.querySelector("#test_data");
const limitInput = document.querySelector("#limit");
const progressRing = document.querySelector('.progress-ring circle');
const timericon =  document.getElementById("timericon");
const progressText = document.getElementById('progress-text');
const quizCourse= document.getElementById("quiz-category");
const quizTimerEl= document.getElementById("quiz-timer");
const quizLevelEl= document.getElementById("quiz-level");
const quizNumberEl= document.getElementById("quiznumber");
const quizQuestionEl= document.getElementById("quizquestion");
const quizNumTab= document.getElementById("questiontabs");
const answersCont= document.getElementById("answersholder");
const nextQuestionBtn= document.getElementById("next");
const prevQuestionBtn= document.getElementById("prev");
const quizResultPopup = document.querySelector(".quizsettingspopup");
/* Result Pop Panel */
const resultdisplaypanel = document.querySelector(".resultdisplaypanel");
const quizretakebtn = document.getElementById("quizretakebtn");
const quizpageredirectbtn = document.getElementById("quizpageredirectbtn");


// Stop timer when data is being submited and also auto submit when timer end

var progressstart=0;
var currentprogress=0;
var calctime=5*limitInput.value;
try {
   var data = JSON.parse(dataInput.value);
} catch (error) {
   alert('You have refreshed the page.\nThis quiz session ends here...');
   window.location.href= `/accounts/user/${document.getElementById("username").textContent}/quiz/`
}
dataInput.value = "";
var question_num = 0;
var subdata = {
   'questions': {
      'id': '',
      'questions': limitInput.value
   }
};
var quizTimer = 5;
var timerFunc = "";

let timerTracker;

quizTimerEl.textContent= convertSecondsToTime(calctime)
function updateProgress() {
   currentprogress=((progressstart/calctime)*100);
 
  progressText.textContent = `${convertSecondsToTime(progressstart)}`;
  progressRing.style.strokeDashoffset = 0 + ((currentprogress/100) * 628.32);
   
  progressstart++;
  
  if (progressstart <= calctime) {
    timerTracker= setTimeout(updateProgress, 1000);
  }else{
     progressRing.style.fill = "var(--primitivecolor)";
     progressText.textContent = "Time Up";
     timericon.style.color = "var(--primarycolor)";
     progressText.style.color = "var(--primarycolor)";
     submitAns(subdata);
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


//Displaying number of questions to be answered
for(x in data){
   quizNumTab.innerHTML += `<span class="qnumb">${parseInt(x)+1}</span>`
}

var question_num= 0;
const optionsList= ['A','B','C','D','E','F']
const next_question = (question_num) => {
   const upperProgresQuestionNumberEl= quizNumberEl.querySelector('span:nth-child(1)')
   const question_to_display = data[question_num].question;
   const answers = data[question_num].answers;
   const displayQuestion= quizQuestionEl.querySelector("h1");
   upperProgresQuestionNumberEl.textContent= `Progress: ${question_num + 1}/${limitInput.value}`
   quizNumTab.querySelector(`span:nth-child(${parseInt(question_num)+1})`).classList.add('active')
   displayQuestion.innerText= question_to_display;
   answersCont.innerHTML= ''
   answers.forEach((ans, index) => {
      answersCont.innerHTML += `<div class="option"><span>${optionsList[index]}</span>${ans}</div>`
   })
   const answersDiv= answersCont.querySelectorAll('div');
   answersDiv.forEach((child, index) => {
      child.addEventListener('click', function SelectAns(e){
         answersDiv.forEach(x => {
            x.classList.remove('active');
         })
         e.target.classList.add('active');
      })
   })

   // const withoutSpan= answersCont.querySelector('div')
   // console.log(withoutSpan.innerHTML.split('</span>')[1])
   
}

nextQuestionBtn.addEventListener('click', function(){
   let userSelect= answersCont.querySelector('div .active')
   userSelect= userSelect?userSelect.innerHTML.split('</span>')[1]: ''
   userAns(question_num, userSelect)
   if(question_num < (limitInput.value) - 1){
      question_num += 1
      next_question(question_num);
      try {
         const answersDiv= answersCont.querySelectorAll('div');
         answersDiv.forEach((child, index) => {
            if(child.innerHTML.split('</span>')[1] == subdata[question_num].userAns){
               child.classList.add('active');
            }
         })
      } catch (error) {
      }
   }else{
      submitAns(subdata)
   }
})

prevQuestionBtn.addEventListener('click', function(){
   if(question_num > 0 ){
      quizNumTab.querySelector(`span:nth-child(${parseInt(question_num)+1})`).classList.remove('active')
      question_num -= 1
      next_question(question_num);
      const answersDiv= answersCont.querySelectorAll('div');
      answersDiv.forEach((child, index) => {
         if(child.innerHTML.split('</span>')[1] == subdata[question_num].userAns){
            child.classList.add('active');
         }
      })
   }else{
      alert('End')
   }
})

function userAns(question_num, userSelect){
   subdata[question_num] = {
      id: data[question_num].id,
      userAns: userSelect, 
   }
   
}

function quizRetake(category, level, limit){
   $.ajax({
      type: "POST",
      url: `/quizz/initialize/`,
      data: {
         category: category,
         level: level,
         limit: limit,
         csrfmiddlewaretoken: $("input[name=csrfmiddlewaretoken]").val()
      },
      success: function (response) {
         if (response.msg == 'Ready'){
            window.location.href = '/quizz/start/';
         }
      },
      error: function (response) {
        alert("An error occurred");
      },
    });
}

function submitAns(quizData){
   clearTimeout(timerTracker)
   quizResultPopup.classList.toggle("active",true);
   body.style.overflow="hidden";
   $.ajax({
      type: "POST",
      url: "/quizz/validate/",
      data: JSON.stringify({'quizData':quizData,'quizInfo':{'cat':quizCourse.textContent, 'level': quizLevelEl.textContent, 'limit': limitInput.value, 'time': progressText.textContent}}),
      contentType: "application/json; charset=utf-8",
      dataType: "json",
      success: function(data){
         quizResultPopup.classList.toggle("active",false);
         resultdisplaypanel.classList.toggle("active",true);
         quizretakebtn.addEventListener('click',()=>{
            resultdisplaypanel.classList.toggle("active",false);
            quizRetake(quizCourse.textContent, quizLevelEl.textContent, limitInput.value);
         });
         quizpageredirectbtn.addEventListener('click',()=>{
            window.location.href = `/accounts/user/${data.user}/quiz/`;
         });
         document.getElementById("percent").textContent= `${data.result.percentage}%`
         document.getElementById("correctsAns").textContent= `${data.result.valid_answers}`
         document.getElementById("incorrectsAns").textContent= `${data.result.invalid_answers}`
         const text= document.querySelectorAll("#result-text p");
         text[0].textContent= `Dear ${data.user}, here's the result for your Quiz.`
         text[1].textContent= `Keep on improving, you did your best in ${quizCourse.textContent} Quiz.`
      },
      error: function (xhr, status, error) {
        console.error("Error:", error);
        alert(error);
      },
    });
}

next_question(question_num);