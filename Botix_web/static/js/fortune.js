var count_coup = 0;

var keyAdd = function (event) {
    if (event.type = "keydown"){
    	if (event.key == 'Enter'){
    		if (event.target.value == 'key'){

    			count_coup ++;
    			event.target.value = '';

    			affiche = document.getElementById("coupon_state")
    			affiche.innerText = "Validé";
    			affiche.style.color = "green";
    		}
    	}
    	if (event.key == 'Backspace' || event.key == 'Delete'){
    		event.target.value = '';
    	}
    }
};

function OpenChest(element) {

	if (count_coup > 0){

		element.className = "coffre_open";
		const image_coffre = element.getElementsByTagName("img")[0]
		image_coffre.src = "../static/image/coffre_ouvert.png"
		element.getElementsByClassName("coffre_chiffre")[0].remove();

		const content_pop = document.createElement("div");
		content_pop.classList.add("coffre_content");
		content_pop.innerText = "?";
		element.insertBefore(content_pop, image_coffre);

		var id = setInterval(monte, 1);
		var hauteur = 0;
		var marginTop = 120;
	  	function monte() {

		    if (marginTop < 1) {
		      clearInterval(id);
		    } 
		    else {
		    	marginTop -= 2;
			    content_pop.style.marginTop = marginTop + 'px';

			    if (hauteur < 100){
					hauteur += 2; 
			      	content_pop.style.height = hauteur + 'px'; 
			    }

			    if (marginTop % 5 === 0){
			    	content_pop.innerText += "?";
			    	content_pop.style.color = '#'+Math.random().toString(16).substr(-6);
			    }
		    }
		 }

		/* FAIRE EN SORTE QUE CA GROSSISSE APRES ETRE MONTE*/
		/*var largeur = 140;
		var marginLeft = 30;
		var id = setInterval(elargie, 1);
		function elargie() {

		    if (marginTop < 1) {
		      clearInterval(id);
		    } 
		    else {
		    	marginTop -= 2;
			    content_pop.style.marginTop = marginTop + 'px';

			    if (hauteur < 100){
					hauteur += 2; 
			      	content_pop.style.height = hauteur + 'px'; 
			    }
		    }
		 }*/

		setTimeout(function(){
		    window.location.pathname += "/" + String(element.getAttribute('indexValue')) ;
		}, 500);  

	}
	else{
		document.getElementById("keyInput").focus();
		var size = window.getComputedStyle(document.getElementById("coupon_state"), null).getPropertyValue('font-size').split('p')[0];
		size = parseInt(size);
		if (size < 60){
			size += 5 ;
			document.getElementById("coupon_state").style.fontSize = size + "px";
		}
		if (size >= 60){
			document.getElementById("coupon_state").style.textDecoration = "underline";
		}
	}
}

document.addEventListener("DOMContentLoaded", function() {
 	document.getElementById("keyInput").addEventListener("keydown", keyAdd);
});