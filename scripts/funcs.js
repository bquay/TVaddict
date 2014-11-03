function upvote(form, comId){
	var updownInput = document.getElementById('updown');
	updownInput.value = "1";
	var comInput = document.getElementById('comId');
	comInput.value = comId;
	form.submit();
}

function downvote(form, comId){
	var updownInput = document.getElementById('updown');
	updownInput.value = "-1";
	var comInput = document.getElementById('comId');
	comInput.value = comId;
	form.submit();
}