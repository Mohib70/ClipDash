// static/js/play_video.js
document.getElementById('comment-form').addEventListener('submit', function (event) {
    event.preventDefault();

    const commentText = document.getElementById('comment-text').value;

    if (commentText === '') {
        alert('Comment cannot be empty');
    } else {
        // Submit the comment (you can make an API call here if needed)
        alert('Comment posted successfully');
    }
});
