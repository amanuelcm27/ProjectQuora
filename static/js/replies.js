export function view_replies_event() {
  document.addEventListener('DOMContentLoaded', function () {
        document.querySelectorAll('.json-link').forEach(function (link) {
            link.addEventListener('click', function (event) {
                event.preventDefault();
                var comment_pk = link.getAttribute('data-comment-id');
                var targetDiv = document.getElementById(`replies-${comment_pk}`);
                targetDiv.style.display = (targetDiv.style.display === 'none' || targetDiv.style.display === '') ? 'block' : 'none';
                // Make an AJAX request using fetch
                fetch(`/all_replies/${comment_pk}/`)
                    .then(response => response.json())
                    .then(data => {
                        // Update the content of the 'replies' div
                        targetDiv.innerHTML = ''; // Clear existing content
                        data.replies.forEach(reply => {
//                            targetDiv.innerHTML +=
//                            `<p><img src=${reply.avatar}> ${reply.creator} Date Created: ${reply.date_created}</p>
//                            <p>${reply.content}</p>`;
                        var replyContainer = document.createElement('div');
                        var creatorPara = document.createElement('p');
                        creatorPara.innerHTML = `<small><img class="profile rounded-circle" src=${reply.avatar}></small><a href=/profile/${reply.creator_id}/>${reply.creator}</a> - ${reply.date_created} ago`;
                        targetDiv.appendChild(creatorPara);
                        var contentPara = document.createElement('p');
                        contentPara.className = 'card-text';
                        contentPara.style.textIndent = '80px';
                        contentPara.textContent = reply.content;
                        targetDiv.appendChild(contentPara);
//                        targetDiv.appendChild(replyContainer);
                        });
                    })
                    .catch(error => {
                        console.error('Error fetching replies:', error);
                });
            });
        });
});
}



//document.addEventListener('DOMContentLoaded', function () {
//    document.querySelectorAll('.replies').forEach(function (element) {
//        var comment_pk = element.getAttribute('data-comment-id');
//        var targetDiv = document.getElementById(`reply-${comment_pk}`);
//        // Make an AJAX request using fetch
//        fetch(`/all_replies/${comment_pk}/`)
//            .then(response => response.json())
//            .then(data => {
//                // Update the content of the 'replies' div
//                targetDiv.innerHTML = ''; // Clear existing content
//                data.replies.forEach(reply => {
//                    targetDiv.innerHTML += `<p>Creator: ${reply.creator} Date Created: ${reply.date_created} </p>
//                        <p>${reply.content}</p>`;
//                });
//            })
//            .catch(error => {
//                console.error('Error fetching replies:', error);
//            });
//    });
//});
//
