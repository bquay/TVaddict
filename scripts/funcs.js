function upvote(form, comId){
	var updownInput = document.getElementById('updown');
	updownInput.value = "1";
	var comStr = '' + comId
	var comInput = document.getElementById(comStr);
	comInput.value = "1";
	form.submit();
}

function downvote(form, comId){
	var updownInput = document.getElementById('updown');
	updownInput.value = "-1";
	var comStr = '' + comId
	var comInput = document.getElementById(comStr);
	comInput.value = "-1";
	form.submit();
}