document.addEventListener("DOMContentLoaded", function () {
	//on click of each edit button, edit_page function called
	document.querySelectorAll(".editButton").forEach((button) => {
		button.addEventListener("click", edit_page);
	});
	document.querySelectorAll(".saveEdit").forEach((button) => {
		button.addEventListener("click", save_edit);
	});
	document.querySelectorAll(".likePost").forEach((button) => {
		button.addEventListener("click", like_post);
	});
	//checks if the text area of the new post is empty, and if it is
	// sends a alert

	index();
	
});
window.onload = function() {
    const editDivs = document.querySelectorAll('.edit'); // select all the edit divs
    editDivs.forEach(function(editDiv) {
      editDiv.style.display = 'none'; // set the display of each edit div to none
    });
  };

  window.addEventListener('beforeunload', function(event) {
    const editDivs = document.querySelectorAll('.edit'); // select all the edit divs
    editDivs.forEach(function(editDiv) {
      editDiv.style.display = 'none'; // set the display of each edit div to none
    });
  });

function index() {
	// hide the edit div class
	document.querySelectorAll(".edit").forEach((edit) => {
		edit.style.display = "none";
	});
}

function edit_page(event) {
	//const with the post id and content of the post button clicked
	// this had to be done so that the whole edit div could appear relative to each post
	const postId = event.target.getAttribute("data-postid");
	const editSection = document.querySelector(`.edit[data-postid="${postId}"]`);
	const postSection = document.querySelector(`.post[data-postid="${postId}"]`);
	const postContent = event.target.dataset.postcontent;
	const editDiv = document.querySelector(`.edit[data-postid="${postId}"]`);
	const textarea = editDiv.querySelector("textarea");

	//hides and show the edit section
	if (editSection.style.display === "block") {
		editSection.style.display = "none";
		event.target.textContent = "Edit";
		postSection.style.display = "block";
	} else {
		editSection.style.display = "block";
		event.target.textContent = "Cancel";
		postSection.style.display = "none";
		textarea.value = postContent;
	}
}

function save_edit(event) {
	//same thing as the edit_page function
	const user = event.target.getAttribute("data-user");
	const postCreator = event.target.getAttribute("data-postcreator");
	const postId = event.target.getAttribute("data-postid");
	const editDiv = document.querySelector(`.edit[data-postid="${postId}"]`);
	const textareaContent = editDiv.querySelector("textarea").value;

	//need to get the csrf token to be able to update the model
	const csrfToken = document.querySelector('input[name="csrfmiddlewaretoken"]').value;

	//to be able to  hide the edit section after saving it
	const editSection = document.querySelector(`.edit[data-postid="${postId}"]`);
	const postSection = document.querySelector(`.post[data-postid="${postId}"]`);

	if (user === postCreator) {
		fetch(`editPost/${postId}`, {
			method: "PUT",
			headers: {
				"Content-Type": "application/json",
				"X-CSRFToken": csrfToken, // include the CSRF token in the headers
			},
			body: JSON.stringify({
				content: textareaContent,
			}),
		});
	}
	// make all the frontend display changes
	editSection.style.display = "none";
	document.querySelector(".editButton").innerHTML = "EDIT";
	postSection.style.display = "block";
	postSection.querySelector(".content").innerHTML = textareaContent;
}

function like_post(event) {
    //same thing as the edit_page function
    const user = event.target.getAttribute("data-user");
    const postId = event.target.getAttribute("data-postid");
    let likeCount = parseInt(event.target.getAttribute("data-likecount"));

    const likePost = document.querySelector(`.likePost[data-postid="${postId}"]`);
    const postDiv = document.querySelector(`.post[data-postid="${postId}"]`);
    const csrfToken = document.querySelector('input[name="csrfmiddlewaretoken"]').value;
	

    //update the likes by adding the user in the like field
	
    fetch(`likePost/${postId}`, {
        method: "PUT",
        headers: {
            
            "X-CSRFToken": csrfToken, // include the CSRF token in the headers
        },
        body: JSON.stringify({
            likes: user,
        }),
    })
	.then((Response) => {
		return Response.json();
	})
	.then((data) => {
		likeCount = data.like_count;
		
		// make all the frontend display changes
		if (likePost.textContent === "Like") {
			postDiv.querySelector(".likes").innerHTML = likeCount;
			likePost.innerHTML = "Dislike";
			likePost.style.backgroundColor = "#bd2121";
			likePost.style.transition = "background-color 0.3s ease-in-out";
		} else {
			postDiv.querySelector(".likes").innerHTML = likeCount;
			likePost.innerHTML = "Like";
			likePost.style.backgroundColor = "#b17b7b";
			likePost.style.transition = "background-color 0.3s ease-in-out";
		}
	})

}