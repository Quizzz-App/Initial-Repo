const coursesCont= document.getElementById('courses-container');

fetch('/quizz/get-questions-info/')
.then(response => response.json())
.then(response => {
   console.log(response);
   for (keys in response){
      coursesCont.innerHTML += `<div class="item">
                                 <img src=${response[`${keys}`]['img']} alt="" srcset="">
                                 <p class="coursetitle">${keys}</p>
                                 <button class="courseselect">Select Course</button>
                              </div>`
      
   }
   
   const courseselect = [...document.getElementsByClassName("courseselect")];
   const coursetitle = [...document.getElementsByClassName("coursetitle")];
   const quizsettingspopup = document.querySelector(".quizsettingspopup");
   const quizsettingspopupclose = document.querySelector("#quizsettingspopupclose");
   const quizcourseheading = document.getElementById("quizcourseheading");
   const quizcourselevels = document.getElementById("level-options");
   const quizlimitInfo= document.getElementById("limit-info");
   const limitInput= document.getElementById("limit-input")
   const preparenstartquiz = document.getElementById("preparenstartquiz");
   
   courseselect.forEach((coursesel,index)=>{
      coursesel.addEventListener('click',()=>{
         let title= coursetitle[index].textContent
         quizcourseheading.textContent= title;
         quizcourselevels.innerHTML= '';
         for (key in response){
            for (level in response[key]){
               if (level !== 'img' && response[key][level] !== 0 && key === title){
                  quizcourselevels.innerHTML += `<option value="${level}">${level}</option>`
               }
            }
         }
         limitInput.value= '';
         limitInput.placeholder= `Your input must be in the range of 1 - ${response[quizcourseheading.textContent][quizcourselevels.value]}`
         quizsettingspopup.classList.toggle("active",true);
         body.style.overflow="hidden";
      });
   });
   quizsettingspopupclose.addEventListener('click',()=>{
        quizsettingspopup.classList.toggle("active",false);
        body.style.overflow="auto";
   });
   
   preparenstartquiz.addEventListener('click',()=>{
      let limit;
      if(limitInput.value !== ''){
         limit= limitInput.value
      }else{
         limit=response[quizcourseheading.textContent][quizcourselevels.value]
      }
      $.ajax({
         type: "POST",
         url: `/quizz/initialize/`,
         data: {
            category: quizcourseheading.textContent,
            level: quizcourselevels.value,
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
   });

   quizcourselevels.addEventListener('change', function(){
      const userSelect= quizcourselevels.value
      const limit= response[quizcourseheading.textContent][userSelect]
      limitInput.placeholder= `Your input must be in the range of 1 - ${limit}`    
   })
   
}).catch(err=>console.error(err));












