const copytn= document.getElementById("btn-copy");
const refLinkEl= document.getElementById("ref-link");

copytn.addEventListener("click", () => {
    const refLink = refLinkEl.textContent;
    // console.log(refLink);
    navigator.clipboard.writeText(refLink);
    alertPopup(alert[0], "Referral link copied to clipboard!");
    //window.location.reload(); // Reload the page to update the referral link in the clipboard
  });