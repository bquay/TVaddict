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

function disableClick(){
	document.getElementById("submitId").disabled = true;
}

function selectShow(showid){
	var form = document.getElementById('searchShow');
	var TvName = document.getElementById('showselectID');
	TvName.value = showid;
	form.submit();
}
function getEpisode(tvid, date){
	var form = document.getElementById('selectEpisode');
	var EpTVID = document.getElementById('episodeselectTVIDID');
	EpTVID.value = tvid;
	var EpDATE = document.getElementById('episodeselectDATEID');
	EpDATE.value = date;
	form.submit();
}