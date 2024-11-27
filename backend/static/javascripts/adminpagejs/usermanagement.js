
// const usermetview = [...document.getElementsByClassName("usermetview")];
const usermetholder = document.querySelector(".usermetholder");
const usermetpanelclose = document.getElementById("usermetpanelclose");

const deactivatereqview = [...document.getElementsByClassName("deactivatereqview")];
const deactivationreqholder = document.querySelector(".deactivationreqholder");
const deactivationreqpanelclose = document.getElementById("deactivationreqpanelclose");

// usermetview.forEach((usermet,i)=>{
//    usermet.addEventListener('click',()=>{
//       usermetholder.classList.toggle("active",true);
//       body.style.overflowY="hidden";
//    })
// })
usermetpanelclose.addEventListener('click',()=>{
   usermetholder.classList.toggle("active",false);
   body.style.overflowY="auto";
})

deactivatereqview.forEach((reqdetail,i)=>{
   reqdetail.addEventListener('click',()=>{
      deactivationreqholder.classList.toggle("active",true);
      body.style.overflowY="hidden";
   })
})
deactivationreqpanelclose.addEventListener('click',()=>{
   deactivationreqholder.classList.toggle("active",false);
   body.style.overflowY="auto";
})

const tdata= document.querySelectorAll("#tdata");

tdata.forEach((x) => {
    const mtBtn= x.querySelector("td:last-child > button")
    const username= x.querySelector("td:nth-child(2)").textContent
    mtBtn.addEventListener("click", function(){
        fetch(`/accounts/user/${username}/metrics/`)
        .then(response => response.json())
        .then(response => {
            console.log(response)
            // Metrics panel update content
            document.getElementById("uID").textContent= response.userID
            document.getElementById("username").textContent= response.username
            document.getElementById("email").textContent= response.email
            response.is_premium?document.getElementById("premium").textContent='Premium':document.getElementById("premium").textContent='Non-Premium'
            document.getElementById("date_joined").textContent= response.date_joined
            document.getElementById("last_login").textContent= response.last_login
            document.getElementById("total-referrals").textContent= response.tr
            document.getElementById("totalQuiz").textContent= response.qt
            document.getElementById("gqa").textContent= `${response.gqa}%`
            document.getElementById("hs").textContent= `${response.hq}%`
            document.getElementById("walletbalance").textContent= `GH₵ ${response.wb}`
            document.getElementById("totaldeposit").textContent= `GH₵ ${response.td}`
            document.getElementById("totalwidrawal").textContent= `GH₵ ${response.tw}`
            document.getElementById("refEarning").textContent= `GH₵ ${response.tre}`
            
            usermetholder.classList.toggle("active",true);
            body.style.overflowY="hidden";
        })
        .catch(err=>console.log(err))
    })
})