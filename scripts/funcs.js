function upvote(form, comId){
	var buttonId = "upvote" + comId;
	document.getElementById(buttonId).disabled = true;
	var updownInput = document.getElementById('updown');
	updownInput.value = "1";
	var comInput = document.getElementById('comId');
	comInput.value = comId;
	form.submit();
}

function downvote(form, comId){
	var buttonId = "downvote" + comId;
	document.getElementById(buttonId).disabled = true;
	var updownInput = document.getElementById('updown');
	updownInput.value = "-1";
	var comInput = document.getElementById('comId');
	comInput.value = comId;
	form.submit();
}