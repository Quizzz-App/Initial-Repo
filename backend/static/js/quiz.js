const limitSlider= document.querySelector('#limit')
const limitLabel= document.querySelector('#limit-label')


limitSlider.addEventListener('input', function() {
    limitLabel.textContent = `Limit: ${this.value}`;
  });