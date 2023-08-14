let addModal = document.querySelector(".modal");  // ADD MENU ITEM MODAL
let addTrigger = document.querySelector(".addItemBtn");
let closeAddButton = document.querySelector(".close");

function toggleModal() {
  addModal.classList.toggle("show-modal");
}

function windowOnClick(event) {
  if (event.target === addModal) {
    toggleModal();
  }
}

function submitForm(event) {
    event.preventDefault();
    let newItemInput = document.getElementById("newItem");
    let newItemValue = newItemInput.value;
    // Process the newItemValue as needed (e.g., add to a list or send to server)
    console.log("New item:", newItemValue);
  
    // Clear the input field after processing
    newItemInput.value = '';
  
    toggleModal("addMenuItem");
  }
  

addTrigger.addEventListener("click", toggleModal);
closeAddButton.addEventListener("click", toggleModal);
window.addEventListener("click", windowOnClick);

function openModal(modalId) {
  let modal = document.getElementById(modalId);
  if (modal) {
    modal.style.display = "block";
  }
}

// DELETE MENU ITEM MODAL
let modal = document.querySelector(".modal");
let trigger = document.querySelector(".menu-btn");
let closeButton = document.querySelector(".close");

function toggleModal() {
  modal.classList.toggle("show-modal");
}

function windowOnClick(event) {
  if (event.target === modal) {
    toggleModal();
  }
}

trigger.addEventListener("click", toggleModal);
closeButton.addEventListener("click", toggleModal);
window.addEventListener("click", windowOnClick);

function openModal(modalId) {
  let modal = document.getElementById(modalId);
  if (modal) {
    modal.style.display = "block";
  }
}
