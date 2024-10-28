const copyBtn = document.getElementById("cp-reflink");
const btnWithdraw = document.getElementById("btn-withdraw");

copyBtn.addEventListener("click", () => {
  const refLink = document.getElementById("ref-link").textContent;
  console.log(refLink);
  navigator.clipboard.writeText(refLink);
  alert("Referral link copied to clipboard!");
  window.location.reload(); // Reload the page to update the referral link in the clipboard
});

btnWithdraw.addEventListener("click", () => {
  const amount = document.getElementById("withdrawal-amount");
  if (amount.value != "") {
    $.ajax({
      type: "POST",
      url: "/payment/issue-withdrawal/",
      data: {
        amount: amount.value,
      },
      success: function (response) {
        if (response.status == "ok") {
          amount.value = "";
          alert(response.message);
        }
      },
      error: function (response) {
        alert("An error occurred");
      },
    });
  } else {
    alert("Please enter the amount to be withdrawn");
  }
});
