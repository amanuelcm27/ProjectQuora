let currentlyOpenMenu=null;
function attachMenuDrowDown() {
    const menu_buttons = document.querySelectorAll(".menu-btn")
    menu_buttons.forEach((menu_button) => {
        menu_button.addEventListener('click',function(event){
            if(event.currentTarget  === menu_button){
                const menu_item_id = menu_button.getAttribute("id")
                const menu = document.getElementById(`menu-for-${menu_item_id}`)
                if (currentlyOpenMenu && currentlyOpenMenu !== menu) {
                    currentlyOpenMenu.style.display = "none";
                }
                menu.style.display = ( menu.style.display==="block") ? "none" : "block";
                currentlyOpenMenu = menu
            }
        })
    })
}
function attachDeleteEvent() {
    const delete_buttons = document.querySelectorAll(".delete")
    delete_buttons.forEach((button)=> {
        const commentId = button.getAttribute("data-comment-id");
        button.addEventListener('click',function(){
            const delete_modal = document.getElementById(`delete-for-${commentId}`);
            delete_modal.style.display="flex";
            const cancel_modal_buttons = document.querySelectorAll(".cancel-delete")
            cancel_modal_buttons.forEach((cancel_button)=>{
                cancel_button.addEventListener("click",function(){
                    delete_modal.style.display="none";
                })
            })
            const confirmDeleteButtons = document.querySelectorAll('.confirm-delete');
            const commentContainer = document.getElementById(`comment-container-for-${commentId}`);
            confirmDeleteButtons.forEach((confirmDeleteButton)=>{
                confirmDeleteButton.addEventListener('click', function(event) {
                    // Make an AJAX request
                    fetch(`/delete_comment/${commentId}/confirm/`)
                        .then(response => response.json())
                        .then(data => {

                        delete_modal.style.display="none";
                        commentContainer.innerText = "";
                    })
                });
            })
        })
    });
}
function attachEditEvent() {
    const edit_buttons = document.querySelectorAll(".edit")
    edit_buttons.forEach((edit_button)=>{
        edit_button.addEventListener('click',()=> {
            const comment_id = edit_button.getAttribute("data-comment-id");
            const existing_content = document.getElementById(`content-for-${comment_id}`);
            const container = document.getElementById(`update-comment-for-${comment_id}`);
            const form = document.getElementById(`update-comment-form-for-${comment_id}`);
            const textarea = document.getElementById(`update-text-for-${comment_id}`);
            const cancel_button = document.getElementById(`cancel-form-${comment_id}`);
            //        const update_button = document.getElementById(`update-button-${comment_id}`);
            container.style.display = "block";
            textarea.value = existing_content.innerText
            currentlyOpenMenu.style.display = "none";
            existing_content.style.display = "none";
            cancel_button.addEventListener("click",(button)=>{
                button.preventDefault();
                existing_content.style.display = "block";
                container.style.display = "none";
            })
        })
    })
}
import { view_replies_event } from './replies.js';
import { replyEvent } from './comment_reply.js';

function addContentToPage(form,data,answer_id) {
    var comment_container = document.getElementById(`comments-for-${answer_id}`)
    var tempElement = document.createElement('div');
    var new_comment = `
            <div class="comment-container" id="comment-container-for-${data.comment_id}" style="margin:25px 10px;">
            <p>
                <small><img src="${data.avatar}" alt="Profile" class="rounded-circle" style=
                "width:30px;height:30px;border-radius:50%;object-fit:cover;"></small>
                <a href="/profile/${data.creator_id}/">${data.creator}</a>-${data.comment_date} ago
            </p>
            <p class="card-text" id="content-for-${data.comment_id}" style="text-indent:30px;">${data.content}</p>
            <div id="update-comment-for-${data.comment_id}" style="display:none;">
                            <form id="update-comment-form-for-${data.comment_id}" action="{% url 'edit_comment' ${data.comment_id}  %}"
                                  method="post"
                                  style="display: flex;align-items:center;  ">
                                {% csrf_token %}
                                <textarea id="update-text-for-${data.comment_id}" class="form-control auto-expand" rows="1"
                                          placeholder="Add reply ..."
                                          style="border-radius:20px; margin:15px; overflow-y:hidden; resize:none;"
                                          name="content"></textarea>
                                <button id="update-button-${data.comment_id}" class="btn btn-primary"
                                        style="margin-right:5px;border-radius:20px;"
                                        type="submit">Update
                                </button>
                                <button id="cancel-form-${data.comment_id}"
                                        class="btn btn-secondary"
                                        style="margin-left:0px auto;border-radius:20px;">
                                    Cancel
                                </button>
                            </form>
                        </div>
                        <!--update comment form end-->
                        <div style="display:flex; background-color:white;">
                            <button class="replyButton btn" data-target="reply-for-${data.comment_id}" type="button"
                                    style="display:inline; border-radius:25px; margin-left:20px; ">Reply
                            </button>
                            <a class="json-link" data-comment-id="${data.comment_id}">
                                <button class="btn" style="border-radius:25px; margin-left:10px; ">View Replies</button>
                            </a>
                            <div class="menu-dropdown">
                                <div class="menu-options" id="menu-for-${data.comment_id}">
                                    <p class="edit" data-comment-id="${data.comment_id}">Edit comment</p>
                                    <p class="delete" data-comment-id="${data.comment_id}">Delete</p>
                                </div>

                                <button class="btn menu-btn" id="${data.comment_id}">
                                    <i class="fas fa-ellipsis"></i>
                                </button>

                            </div>
                            <div class="delete-modal" id="delete-for-${data.comment_id}">
                                <div class="modal-content">
                                    <h4>Delete</h4>
                                    <p>Are you sure you want to delete this comment?</p>
                                    <button class="btn cancel-delete">Cancel</button>
                                    <button class="btn confirm-delete">Ok</button>
                                </div>
                            </div>
                        </div>
                        <div id="reply-for-${data.comment_id}" style="display:none;">
                            <form id="form-for-${data.comment_id}" action="{% url 'reply' ${data.comment_id} ${answer_id} %}"
                                  method="post"
                                  style="display: flex;align-items:center; ">
                                {% csrf_token %}
                                <textarea id="text-for-${data.comment_id}" class="form-control auto-expand" rows="1"
                                          placeholder="Add reply ..."
                                          style="border-radius:20px; margin:15px; overflow-y:hidden; resize:none;"
                                          name="content"></textarea>
                                <button id="button-${data.comment_id}" class="btn btn-primary"
                                        style="margin-left:0px auto;border-radius:20px;"
                                        type="submit">Reply
                                </button>
                            </form>
                        </div>
                        <div id="replies-${data.comment_id}" style="text-indent:50px;"></div>
            </div>`;
    tempElement.innerHTML = new_comment;
    comment_container.insertBefore(tempElement, form.nextSibling);

}
const comment_forms= document.querySelectorAll(".commentForm");
comment_forms.forEach((form)=>{
    const answer_id = form.getAttribute("data-answer-id");
    const button = document.getElementById(`comment-button-${answer_id}`)
    button.addEventListener("click", (event)=> {
        event.preventDefault();
        var formData = new FormData(form);
        fetch(`comment/${answer_id}/`, {
            method: 'POST',
            headers: {
                'X-Requested-With': 'XMLHttpRequest',
                'X-CSRFToken': formData.get('csrfmiddlewaretoken'), // Include CSRF token in the headers
            },
            body: formData
        }).then(response => response.json())
            .then(data => {
            if (data.fail !== 1) {
                addContentToPage(form,data,answer_id);
                form.reset();
            }
        })
    })
})
function callAllEvent() {
    attachMenuDrowDown();
    attachDeleteEvent();
    attachEditEvent();
    view_replies_event();
    replyEvent();
}
callAllEvent();










