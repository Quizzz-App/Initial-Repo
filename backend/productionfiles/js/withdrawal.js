const btnApprove = document.querySelector("#btn-approve");
const btnDecline = document.querySelector("#btn-decline");
const btnDeposite = document.querySelector("#btn-deposite");
const btnOTP = document.querySelector("#btn-otp");
const issuer = document.querySelector("#issuer");
const issuerID = document.querySelector("#issuerID");
const withdrawalID = document.querySelector("#withdrawalID");
const nftID = document.querySelector("#nftID");
const elOtpTransferCode = document.querySelector("#finialize-transfer");

btnDeposite.addEventListener("click", () => {
  const depositeAmount = prompt("Enter amount to be deposited");
  console.log(depositeAmount);
  // $.ajax({
  //   type: "POST",
  //   url: "/payment/approve-withdrawal/",
  //   data: {
  //     issuer: issuer.value,
  //     nftID: nftID.value,
  //   },
  //   success: function (response) {
  //     if (response.status == "ok") {
  //       amount.value = "";
  //       alert(response.message);
  //     }
  //   },
  //   error: function (response) {
  //     alert("An error occurred");
  //   },
  // });
});

btnOTP.addEventListener("click", () => {
  const OTPCode = document.querySelector("#otp");
  const elOtpTransferCode = document.querySelector("#otp_transferCode");
  const elOtp = document.querySelector("#finialize-transfer");
  elOtp.classList.remove("non-hide");
  elOtp.classList.add("hide");
  $.ajax({
    type: "POST",
    url: "/payment/finalize-withdrawal/",
    data: {
      otp: OTPCode.value,
      transferCode: elOtpTransferCode.value,
      nftID: nftID.value,
    },
    success: function (response) {
      window.location.href = "/accounts/notifications/";
      console.log(response);
    },
    error: function (response) {
      alert("An error occurred");
    },
  });
});

btnApprove.addEventListener("click", () => {
  $.ajax({
    type: "POST",
    url: "/payment/approve-withdrawal/",
    data: {
      issuer: issuer.value,
      issuerID: issuerID.value,
      nftID: nftID.value,
      withdrawalID: withdrawalID.value,
    },
    success: function (response) {
      if (response.status == "ok") {
        const elOtp = document.querySelector("#finialize-transfer");

        const elOtpTransferCode = document.querySelector("#otp_transferCode");
        elOtpTransferCode.value = response.transferCode;
        elOtp.classList.remove("hide");
        elOtp.classList.add("non-hide");
        // elOtp.style.display = "block";
        alert(response.message);
        console.log(elOtpTransferCode.classList);

        console.log(response);
      }
    },
    error: function (response) {
      alert("An error occurred");
    },
  });
});

btnDecline.addEventListener("click", () => {
  const reason = prompt("Please provide reason");
  if (reason == "") {
    alert("Please provide a reason");
    return;
    urn;
  } else {
    $.ajax({
      type: "POST",
      url: "/payment/decline-withdrawal/",
      data: {
        reason: reason,
        issuer: issuer.value,
        nftID: nftID.value,
      },
      success: function (response) {
        if (response.status == "ok") {
          alert(response.message);
          window.location.href = `/accounts/notifications/`;
        }
      },
      error: function (response) {
        alert("An error occurred");
      },
    });
  }
});
