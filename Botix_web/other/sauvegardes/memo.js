function EmptyBox() {
	document.getElementById("SearchSubjectInput").value = "";
}

let profiles = ["Deltix#4040 - 174112128548995072","SaHes#0484 - 130406141195714560","leauhic#2803 - 213383149906952192"];

function UpdateProfile(){
	const datalist = document.getElementById("saved_profile");
	datalist.innerHTML = '';

	for (profile of profiles){
		const option = document.createElement('option');
		option.innerText = profile;
		datalist.appendChild(option)
	}
}

function SaveProfile(){
	const profile = document.getElementById("SearchSubjectInput").value;
	if ((!profiles.includes(profile)) && profile.split(' ').length==3){
		const id = profile.split(' ')[2];
		if (id.length == 18){
			profiles.push(profile)
		}
	}
	UpdateProfile();
}

// S'execute au chargement de la page
document.addEventListener("DOMContentLoaded", function() {
 	UpdateProfile();
});