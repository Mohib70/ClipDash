const form = document.getElementById('upload-video-form');

form.addEventListener('submit', function (event) {
    event.preventDefault();

    const formData = new FormData(form);

    fetch('/upload_video/', {
        method: 'POST',
        headers: {
            'X-CSRFToken': form.querySelector('[name=csrfmiddlewaretoken]').value,
        },
        body: formData,
    })
        .then((response) => {
            if (!response.ok) {
                throw new Error('Network response was not ok');
            }
            return response.json();
        })
        .then((data) => {
            if (data.success) {
                document.getElementById('upload-success-message').style.display = 'block';
                alert('Video uploaded successfully!');
            } else {
                alert('Error uploading video: ' + data.error);
            }
        })
        .catch((error) => {
            console.error('Error uploading video:', error);
            alert('An error occurred. Please try again.');
        });
});
