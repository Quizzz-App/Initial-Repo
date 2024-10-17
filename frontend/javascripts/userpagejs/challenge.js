
const takechallengeoption = document.getElementById("takechallengeoption");
const challengespanel = document.querySelector(".challengespanel");
const challengepanelclose = document.getElementById("challengepanelclose");

const optionbtn = [...document.getElementsByClassName("optionbtn")];
const challengecontent = [...document.getElementsByClassName("challengecontent")];

const challengedetailviewbtn = [...document.querySelectorAll("#challengedetailviewbtn")];
const challengedetailspanel = document.querySelector(".challengedetailspanel");
const detailholderclose = document.getElementById("detailholderclose");

const createchallengeoption = document.getElementById("createchallengeoption");
const challengesettingspanel = document.querySelector(".challengesettingspanel");
const challengesettingspanelclose = document.getElementById("challengesettingspanelclose");

const challengemetricsview = [...document.getElementsByClassName("challengemetricsview")];
const challengeoutcome = document.querySelector(".challengeoutcome");
const challengeoutcomeclose = document.getElementById("challengeoutcomeclose");

takechallengeoption.addEventListener('click',()=>{
    challengespanel.classList.toggle("active",true);
    body.style.overflowY = "hidden"
});
challengepanelclose.addEventListener('click',()=>{
   challengespanel.classList.toggle("active",false);
   body.style.overflowY = "auto"
});

optionbtn[0].addEventListener('click',()=>{
   optionbtn[0].classList.toggle("active",true);
   optionbtn[1].classList.toggle("active",false);
   optionbtn[2].classList.toggle("active",false);
   challengecontent[0].classList.toggle("active",true);
   challengecontent[1].classList.toggle("active",false);
   challengecontent[2].classList.toggle("active",false);
});
optionbtn[1].addEventListener('click',()=>{
   optionbtn[0].classList.toggle("active",false);
   optionbtn[1].classList.toggle("active",true);
   optionbtn[2].classList.toggle("active",false);
   challengecontent[0].classList.toggle("active",false);
   challengecontent[1].classList.toggle("active",true);
   challengecontent[2].classList.toggle("active",false);
});
optionbtn[2].addEventListener('click',()=>{
   optionbtn[0].classList.toggle("active",false);
   optionbtn[1].classList.toggle("active",false);
   optionbtn[2].classList.toggle("active",true);
   challengecontent[0].classList.toggle("active",false);
   challengecontent[1].classList.toggle("active",false);
   challengecontent[2].classList.toggle("active",true);
});


challengedetailviewbtn.forEach((viewbtn) => {
    viewbtn.addEventListener('click',() => {
       challengedetailspanel.classList.toggle("active",true);
    });
});
detailholderclose.addEventListener('click',()=>{
   challengedetailspanel.classList.toggle("active",false);
});


createchallengeoption.addEventListener('click',()=>{
    challengesettingspanel.classList.toggle("active",true);
    body.style.overflowY = "hidden"
});
challengesettingspanelclose.addEventListener('click',()=>{
    challengesettingspanel.classList.toggle("active",false);
    body.style.overflowY = "auto"
});


challengemetricsview.forEach((metricsview)=>{
   metricsview.addEventListener('click',()=>{
      challengeoutcome.classList.toggle("active",true);
      body.style.overflowY = "hidden"
   })
});
challengeoutcomeclose.addEventListener('click',()=>{
   challengeoutcome.classList.toggle("active",false);
    body.style.overflowY = "auto"
});
