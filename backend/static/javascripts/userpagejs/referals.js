const copyBtn= document.getElementById("btn-copy");
const refLinkEl= document.getElementById("ref-link");

copyBtn.addEventListener("click", () => {
    const refLink = refLinkEl.textContent;
    console.log(refLink);
    navigator.clipboard.writeText(refLink);
    alert("Referral link copied to clipboard!");
    //window.location.reload(); // Reload the page to update the referral link in the clipboard
  });