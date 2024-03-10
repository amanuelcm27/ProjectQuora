export function replyEvent() {
    var replyButtons = document.querySelectorAll('.replyButton');
    replyButtons.forEach(function(button) {
        button.addEventListener('click', function() {
            var targetId = button.getAttribute('data-target');
            var form = document.getElementById(targetId);
            form.style.display = (form.style.display === 'none' || form.style.display === '') ? 'block' : 'none';
        });
    });
}
document.addEventListener('DOMContentLoaded', function() {
    var commentButtons = document.querySelectorAll('.commentButton');
    commentButtons.forEach(function(button) {
        button.addEventListener('click', function() {
            var targetId = button.getAttribute('data-target');
            var form = document.getElementById(targetId);
            form.style.display = (form.style.display === 'none' || form.style.display === '') ? 'block' : 'none';
        });
    });

    var textareas = document.querySelectorAll('.auto-expand');

    textareas.forEach(function(textarea) {
        textarea.addEventListener('input', function() {
            this.style.height = 'auto';
            this.style.height = (this.scrollHeight) + 'px';
        });
    });
});
