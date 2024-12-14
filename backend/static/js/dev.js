const verifyBtn= document.getElementById("verify")

verifyBtn.addEventListener("click", function(){
    const username= document.getElementById("username");
    const email= document.getElementById("email");
    const ref= document.getElementById("ref")
    const msg= document.getElementById("msg")

    let formData= new FormData();

    formData.append("username", username.value)
    formData.append("email", email.value)
    formData.append("ref", ref.value)

    fetch('/verify-transaction/', {
        method: "POST",
        body: formData,
    }).then(response => response.json())
    .then(response => {
        console.log(response)
        if (response.code == 200){
            alertPopup(alert[0], response.msg)
            msg.textContent= response.msg
        }else{
            alertPopup(alert[1], response.msg)
            msg.textContent= response.msg
        }
    }).catch(err => {
        console.error(err)
        alertPopup(alert[1], err)
        msg.textContent= err
    })
})