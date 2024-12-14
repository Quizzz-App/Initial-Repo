const containerEl = document.querySelectorAll(".refs");
const elID = document.querySelector("#payment-id");

containerEl.forEach((div) => {
  const nftID = div.querySelector("#nft-id");
  const completedBtn = div.querySelector("#btn-completed");

  completedBtn.addEventListener("click", () => {
    $.ajax({
      type: "POST",
      url: "/payment/completed-transfer/",
      data: {
        nftID: nftID.value,
        ID: elID.value,
      },
      success: function (response) {
        completedBtn.textContent = "Done";
        completedBtn.disabled = true;
        alert(response.message);
      },
      error: function (response) {
        alert("An error occurred");
      },
    });
  });
});
