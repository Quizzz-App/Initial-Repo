const elAmount = document.querySelector("#Tamount");
const elSelected = document.querySelector("#selected");
const elRequests = document.querySelectorAll(".refs");
const elContentDiv = document.querySelector(".messages-container");
const elSubmit = document.querySelector("#submit-list");
const elDP = document.querySelector("#dP-btns");

var Tamount = 0;
var SelectedUsers = 0;
var selectUserList = [];

function UpdateInfo() {
  elAmount.textContent = `Total amount: ${Tamount}`;
  elSelected.textContent = `Selected Users: ${SelectedUsers}`;
  elAmount.addEventListener;
}

function selectUser(btn, name, amount) {
  if (btn.textContent == "Select") {
    btn.textContent = "Deselect";
    Tamount += parseInt(amount.value);
    selectUserList.push(`${name.value}`);
  } else {
    btn.textContent = "Select";
    Tamount -= parseInt(amount.value);
    selectUserList = selectUserList.filter((item) => item !== name.value);
  }
  SelectedUsers = selectUserList.length;
  UpdateInfo();
  console.log(selectUserList);
}

function declineRequest(issuer, nftID, div) {
  const reason = prompt("Please provide reason");
  if (reason == "") {
    alert("Please provide a reason");
    return;
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
          div.style.display = "none";
          console.log(response);
        }
      },
      error: function (response) {
        alert("An error occurred");
      },
    });
  }
}

elRequests.forEach((x, index) => {
  const selectBtn = x.querySelector("#btn-select");
  const declineBtn = x.querySelector("#btn-decline");
  const issuerName = x.querySelector("#issuer-name");
  const issuerAmount = x.querySelector("#issuer-amount");
  const nftID = x.querySelector("#nft-id");

  selectBtn.addEventListener("click", () => {
    selectUser(selectBtn, nftID, issuerAmount);
  });
  declineBtn.addEventListener("click", () => {
    declineRequest(issuerName, nftID, x);
  });
});

elSubmit.addEventListener("click", (e) => {
  if (e.target.textContent == "Processing...Pleas wait") {
    alert("There's a task in session...");
  }
  const data = selectUserList;
  e.target.textContent = "Processing...Pleas wait";
  $.ajax({
    type: "POST",
    url: "/payment/payment-method-manual-list/",
    data: {
      nftIDs: JSON.stringify(selectUserList),
    },
    success: function (response) {
      if (response.status == "ok") {
        if (response.message == "You failed to select a user") {
          e.target.textContent = "Submit list";
          alert(`${response.message}\nNo sheet file was created`);
        } else if (response.message == "Invalid data entry") {
          e.target.textContent = "Submit list";
          alert(response.message);
        } else {
          e.target.style.display = "none";
          elDP.classList.replace("hide", "non-hide");
          const downloadBtn = elDP.querySelector("#btn-download");
          const printBtn = elDP.querySelector("#btn-print");

          printBtn.addEventListener("click", function () {
            printFile(response.path);
          });

          downloadBtn.href = response.path;
          disableBtns(elContentDiv);
          // downloadBtn.addEventListener("click", function (e) {
          //   e.target.href = response.path;
          // });
        }
        console.log(response);
      }
    },
    error: function (response) {
      alert("An error occurred");
    },
  });
});

const disableBtns = (elment) => {
  const btns = elment.querySelectorAll("button");
  btns.forEach((btn) => {
    btn.disabled = true;
    btn.classList.add("disabled");
  });
};

const printFile = (url) => {
  // const windowRef = window.open(url, "_blank");
  // windowRef.onload = () => {
  //   windowRef.focus();
  //   windowRef.print();
  // //   windowRef.close();
  // };
  // const blobURL = URL.createObjectURL(url);
  // const iframe = document.createElement("iframe");
  // iframe.style.display = "none";
  // iframe.src = url;
  // document.body.appendChild(iframe);
  // iframe.onload = () => {
  //   iframe.contentWindow.focus();
  //   iframe.contentWindow.print();
  //   document.body.removeChildChild(iframe);
  // };
  // setTimeout(() => {
  //   iframe.contentWindow.print();
  //   iframe.parentNode.removeChild(iframe);
  // }, 1000);

  fetch(url)
    .then((reponse) => reponse.blob())
    .then((blob) => {
      const fileUrl = URL.createObjectURL(blob);
      window.open(fileUrl, "_blank");
    })
    .catch((err) => {
      console.error(err);
    });
};
