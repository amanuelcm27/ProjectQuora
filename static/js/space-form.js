const space_container = document.querySelector(".space-container");
const create_space_button = document.getElementById("create-space-btn");
const close_space = document.getElementById("close-space-form");


create_space_button.addEventListener('click',()=> {
    space_container.style.display = "flex";
    close_space.addEventListener("click",()=> {
        space_container.style.display = "none";
    })
})