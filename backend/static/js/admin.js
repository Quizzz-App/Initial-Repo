const el = document.querySelector(".more-info-users > p");
const elTable = document.querySelector(".more-info-users > table");

const elW = document.querySelector(".more-info-wallet > p");
const elTableW = document.querySelector(".more-info-wallet > table");

el.addEventListener("click", () => {
  if (elTable.classList.contains("non-hide")) {
    elTable.classList.remove("non-hide");
    elTable.classList.add("hide");
    el.textContent = "Show more info on users";
  } else {
    elTable.classList.remove("hide");
    elTable.classList.add("non-hide");
    el.textContent = "Show less info on users";
  }
});

elW.addEventListener("click", () => {
  // if (elTableW.classList.contains("non-hide")) {
  //   elTableW.classList.remove("non-hide");
  //   elTableW.classList.add("hide");
  //   elW.textContent = "Show more info on wallet";
  // } else {
  //   elTableW.classList.remove("hide");
  //   elTableW.classList.add("non-hide");
  //   elW.textContent = "Show less info on wallet";
  // }
  if (elTableW.classList.contains("hide")) {
    elTableW.classList.remove("hide");
    elTableW.style.display = "table";
    elW.textContent = "Show more info on wallet";
  } else {
    elTableW.style.display = "";
    elTableW.classList.add("hide");
    elW.textContent = "Show less info on wallet";
  }
});
