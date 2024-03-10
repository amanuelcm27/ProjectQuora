document.addEventListener('DOMContentLoaded', function () {
        document.querySelectorAll('.upvote-button').forEach(function(button) {
            button.addEventListener('click', function(event) {
                event.preventDefault();
                var pk = this.getAttribute('data-pk');
                var flag = this.getAttribute('data-flag');
                // Send an Ajax request to the upvote_downvote_answer view
                // Update the upvote count in the DOM
                fetch(`/upvote_downvote/${pk}/${flag}/`)
                    .then(response => response.json())
                    .then(data => {
                        var upvoteCountElement = document.getElementById(`upvote-count-${pk}`);
                        upvoteCountElement.innerText = data.upvote_count;
                        var downvoteCountElement = document.getElementById(`downvote-count-${pk}`);
                        downvoteCountElement.innerText = data.downvote_count;
                    });
            });
        });
        document.querySelectorAll('.downvote-button').forEach(function(button) {
            button.addEventListener('click', function(event) {
                event.preventDefault();
                var pk = this.getAttribute('data-pk');
                var flag = this.getAttribute('data-flag');

                fetch(`/upvote_downvote/${pk}/${flag}/`)
                    .then(response => response.json())
                    .then(data => {
                        var downvoteCountElement = document.getElementById(`downvote-count-${pk}`);
                        downvoteCountElement.innerText = data.downvote_count;
                        // Decrement the upvote count in real-time
                        var upvoteCountElement = document.getElementById(`upvote-count-${pk}`);
                        upvoteCountElement.innerText = data.upvote_count;
                    });
            });
        });

    });

