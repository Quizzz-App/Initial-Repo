const message_list = document.querySelectorAll(".messages-container > .items");

message_list.forEach((item) => {
  const btns = item.querySelector("button");
  const nftID = item.querySelector("#nft-id");
  const itemDiv = item.querySelector("a");
  const statusEl = item.querySelector("#status-el");
  btns.addEventListener("click", function (e) {
    readNotification(nftID.value, e, statusEl);
  });
  itemDiv.addEventListener("click", function () {
    const nftID = this.id;
    $.ajax({
      type: "POST",
      url: `/accounts/notifications-update/`,
      data: {
        nftID: nftID,
        csrfmiddlewaretoken: $("input[name=csrfmiddlewaretoken]").val(),
      },
      success: function (response) {
        if (response.status === "ok") {
          //read
          console.log(`${response.id}`);
        } else {
          //pass
          console.log(`${response.id}`);
        }
      },
      error: function (response) {
        alert("An error occurred");
      },
    });
  });
});

function readNotification(id, e, statusEl) {
  $.ajax({
    type: "POST",
    url: `/accounts/notifications-update/`,
    data: {
      nftID: id,
      csrfmiddlewaretoken: $("input[name=csrfmiddlewaretoken]").val(),
    },
    success: function (response) {
      if (response.status === "ok" || response.status === "not_ok") {
        //read
        const btn = e.target;
        btn.textContent = "Read";
        btn.setAttribute("disabled", "");
        statusEl.textContent = "Status: Read";
        // window.location.href = '/accounts/notifications/';
      } else {
        //pass
        console.log(`${response.id}`);
      }
    },
    error: function (response) {
      alert("An error occurred");
    },
  });
}
