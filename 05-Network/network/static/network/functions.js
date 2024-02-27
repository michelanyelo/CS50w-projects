function getCookie(name) {
    const value = `; ${document.cookie}`;
    const parts = value.split(`; ${name}=`);
    if (parts.length == 2) return parts.pop().split(';').shift();

}

function submit_changes(id) {
    const postContent = document.getElementById(`textarea_${id}`).value;
    const content = document.getElementById(`postContent_${id}`);
    const edit_modal = document.getElementById(`editPost_${id}`);
    const modal = bootstrap.Modal.getInstance(edit_modal);
    fetch(`/edit/${id}`, {
        method: "POST",
        headers: { "Content-type": "application/json", "X-CSRFToken": getCookie("csrftoken") },
        body: JSON.stringify({
            content: postContent,
        })
    })
        .then(response => response.json())
        .then(result => {
            console.log(result);
            content.innerHTML = result.data;
            modal.hide();
        })
}

function likeHandler(postId, likedPostsIds) {
    var likeButton = document.getElementById('like_' + postId);
    var isLiked = likedPostsIds.includes(postId);

    if (isLiked) {
        fetch(`/remove_like/${postId}`)
            .then(response => response.json())
            .then(result => {
                likeButton.innerHTML = '<i class="fa-solid fa-thumbs-up"></i> Like';
                likeButton.classList.remove('dislike');
                likeButton.classList.add('like');
                likedPostsIds.splice(likedPostsIds.indexOf(postId), 1);
                location.reload();
            });
    } else {
        fetch(`/add_like/${postId}`)
            .then(response => response.json())
            .then(result => {
                likeButton.innerHTML = '<i class="fa-solid fa-thumbs-down"></i> Dislike';
                likeButton.classList.remove('like');
                likeButton.classList.add('dislike');
                likedPostsIds.push(postId);
                location.reload();
            });
    }
}



