const nameInput = document.querySelector("#name");
const dataInput = document.querySelector("#test_data");
const limitInput = document.querySelector("#limit");
const questionText = document.querySelector("#question-text");
const submitAnsBtn = document.querySelector(".read-btn");

var data = JSON.parse(dataInput.value);
dataInput.value = "";
var limit = limitInput.value;
var question_num = 0;
var subdata = {};
var quizTimer = 5;
var timerFunc = "";

console.log(data);
const beforeUnloadHandler = (event) => {
  // Recommended
  event.preventDefault();

  // Included for legacy support, e.g. Chrome/Edge < 119
  event.returnValue = true;
};

const next_question = (num) => {
  const answersContainer = document.querySelector(".answers");
  const question_to_display = data[num].question;
  const answers = data[num].answers;

  questionText.textContent = `${num + 1}. ${question_to_display}`;
  answersContainer.innerHTML = "";
  quizTimer = 20;
  for (_ in answers) {
    // Create a div
    const ansDiv = document.createElement("div");
    ansDiv.className = "ans-div";

    // Create a new radio element
    const radioElement = document.createElement("input");
    radioElement.type = "radio";
    radioElement.name = "answers-input";
    radioElement.value = answers[_];
    radioElement.id = answers[_];
    if (_ == 0) {
      radioElement.checked = true;
    }

    // Append the radio element to the div
    ansDiv.appendChild(radioElement);

    // Create a label for the radio element
    const labelElement = document.createElement("label");
    labelElement.textContent = answers[_];
    labelElement.setAttribute("for", radioElement.id);
    ansDiv.appendChild(labelElement);

    // Append the label to the div
    answersContainer.appendChild(ansDiv);
  }
};

function receive_ans() {
  const userAnswers = document.querySelectorAll('input[name="answers-input"]');
  let userAnswer = "";
  for (_ in userAnswers) {
    if (userAnswers[_].checked) {
      userAnswer = userAnswers[_].value;
      break;
    }
  }
  let question_id = data[question_num].id;
  subdata[question_num] = {
    id: question_id,
    userAns: userAnswer,
  };
  console.log(subdata);
  question_num += 1;
  if (question_num >= limit) {
    submitAnsBtn.removeEventListener("click", receive_ans);
    clearInterval(timerFunc);
    submitAns(subdata);
  } else {
    next_question(question_num);
  }
}

const submitAns = (data) => {
  console.log(data);
  $.ajax({
    type: "POST",
    url: "/quizz/test/validate/",
    data: JSON.stringify(data),
    contentType: "application/json; charset=utf-8",
    dataType: "json",
    success: function (data) {
      const resultContainer = document.querySelector(".question-card");
      const header = document.querySelector(".header");

      resultContainer.innerHTML = "";
      header.innerHTML = "";
      // Creating Resuslt element
      const resultHeader = document.createElement("h2");
      const resultel1 = document.createElement("h3");
      const resultel2 = document.createElement("h3");
      const score = document.createElement("h3");
      const retakeQuiz = document.createElement("a");

      resultHeader.id = "quiz-result";
      resultHeader.textContent = "Quiz Result";

      resultel1.textContent = `Correct Answers: ${data.result.valid_answers}`;
      resultel2.textContent = `Incorrect Answers: ${data.result.invalid_answers}`;
      score.textContent = `Your Score: ${data.result.percentage.toFixed(1)}%`;

      retakeQuiz.textContent = "Retake Quiz";
      retakeQuiz.href = "/quizz/test/";
      retakeQuiz.classList.add("read-btn");

      resultContainer.appendChild(resultHeader);
      resultContainer.appendChild(resultel1);
      resultContainer.appendChild(resultel2);
      resultContainer.appendChild(score);
      resultContainer.appendChild(retakeQuiz);
      reset();
    },
    error: function (xhr, status, error) {
      console.error("Error:", error);
    },
  });
};

const timer = () => {
  const timerEl = document.querySelector(".header > h3");
  quizTimer -= 1;
  if (question_num < limit) {
    if (quizTimer < 0) {
      receive_ans();
    }
  }
  timerEl.textContent = `Timer: ${quizTimer}s`;
};
const reset = () => {
  question_num = 0;
  subdata = {};
  quizTimer = 21;
  timerFunc = "";
};

submitAnsBtn.addEventListener("click", receive_ans);

nameInput.addEventListener("", (event) => {
  if (event.target.value === "") {
    window.addEventListener("beforeunload", beforeUnloadHandler);
    console.log("prevent");
  } else {
    window.removeEventListener("beforeunload", beforeUnloadHandler);
  }
});

document.addEventListener("visibilitychange", () => {
  console.log(document.visibilityState);
  // Modify behavior…
});

next_question(question_num);
submitAnsBtn.classList.remove("hide");
timerFunc = setInterval(timer, 1000);
