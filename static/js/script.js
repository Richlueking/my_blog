
const dropdownMenu = document.querySelector(".dropdown-menu");
const dropdownButton = document.querySelector(".dropdown-button");

if (dropdownButton) {
  dropdownButton.addEventListener("click", () => {
    dropdownMenu.classList.toggle("show");
  });
}

const dropdownMenu_delete = document.querySelector(".layout__box_delete");
const dropdownButton_delete = document.querySelector(".delete-blog");

if (dropdownButton_delete) {
  dropdownButton_delete.addEventListener("click", () => {
    dropdownMenu_delete.classList.toggle("show");
  });
}

///////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////

/*
const dropdownButton_confirm = document.querySelector(".btn--main");
const dropdownButton_confirm_cancel = document.querySelector(".cancel_delete")

if (dropdownButton_confirm) {
  dropdownButton_confirm.addEventListener("click", () => {
    dropdownMenu_delete.classList.toggle("hide");
  });
}
*/

// Upload Image
const photoInput = document.querySelector("#avatar");
const photoPreview = document.querySelector("#preview-avatar");
if (photoInput)
  photoInput.onchange = () => {
    const [file] = photoInput.files;
    if (file) {
      photoPreview.src = URL.createObjectURL(file);
    }
  };

// Scroll to Bottom
const conversationThread = document.querySelector(".room__box");
if (conversationThread) conversationThread.scrollTop = conversationThread.scrollHeight;


