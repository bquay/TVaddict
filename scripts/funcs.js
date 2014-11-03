function upvote(form){
	var updownInput = document.getElementById('updown');
	updownInput.value = "1";
	form.submit();
}

function downvote(form){
	var updownInput = document.getElementById('updown');
	updownInput.value = "-1";
	form.submit();
}