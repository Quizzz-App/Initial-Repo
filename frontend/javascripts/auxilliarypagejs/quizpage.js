
const progressRing = document.querySelector('.progress-ring circle');
const progressText = document.getElementById('progress-text');

var progressstart=0;
var currentprogress=0;

var calctime=1*10;

function updateProgress() {
   currentprogress=((progressstart/calctime)*100);
 
  progressText.textContent = `${convertSecondsToTime(progressstart)}`;
  progressRing.style.strokeDashoffset = 0 + ((currentprogress/100) * 630);
   
  progressstart++;
  
  if (progressstart <= calctime) {
    setTimeout(updateProgress, 1000);
  }else{
     console.log("complete");
     progressRing.style.fill = "var(--primitivecolor)";
     progressText.textContent = "Time Up";
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