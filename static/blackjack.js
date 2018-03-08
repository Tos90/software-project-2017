 var width;
var height;
var interval_id;
 var dealer;
+var prev_wallet;
/* starting coordinates for player 1 cards*/
var player1 = {
	card1x:565,
@ -40,12 +37,26 @@ document.addEventListener('DOMContentLoaded', init, false);
function init() {  
	canvas = document.querySelector('canvas');
	context = canvas.getContext('2d')
+
	table();

		$.ajax({
		url: "/newhand",
		type: 'GET',
		success: function(response){
			alert(response);
		},
		error: function(error) {
			alert('error');
		}
	});
	//event listeners to react to button presses
	document.getElementById("myBet").addEventListener("click",betValue);		
	document.getElementById("bet").addEventListener("click",placeBet);
+	document.getElementById("newGame").addEventListener("click",newhand);
}
setInterval(getDB,1000);
setTimeout(dealersTurn,30000);
function betValue(){

	var slider = document.getElementById("myBet");
@ -59,7 +70,7 @@ function betValue(){
	return(output.innerHTML);
}
function placeBet(){
+	// get player id from python script here
	//allow player to make a bet 
	//link betting code form python here

@ -67,10 +78,12 @@ function placeBet(){

	$.ajax({
		url: "/betting",
+		data: JSON.stringify("bet" : myData),
		type: 'POST',
		success: function(response){
			alert(response);
			var wallettop = document.getElementById('wallet');
			wallettop.innerHTML = "Wallet: "+(response);
		},
		error: function(error) {
			alert(error);
@ -79,25 +92,14 @@ function placeBet(){
	//update the bet field at top of screen
	var bettop = document.getElementById('betPlaced');
	bettop.innerHTML = "Your Bet: "+betValue();
	//disable bet button until new game has started
	document.getElementById("bet").disabled=true;	

 	// will become redundant once code is fully linked with server and database
	var chip = document.createElement("div");
	var bet=  document.createTextNode(betValue());
+	chip.id="chip"+z;//4 will be replaced by player id
	chip.className="chip";
	chip.appendChild(bet);
	document.getElementById("canvas-container").appendChild(chip);
@ -252,40 +254,11 @@ function placeBet(){

		// check if final card has been dealt to player 4
		if(player4.card2y == 455){
 			choicePhase()
		}
	}
	interval_id=setInterval(movecards, 10);
 }	
 function choicePhase(){


@ -297,7 +270,6 @@ function choicePhase(){
	    context.drawImage(imageObj, 560, 0, 80, 129); //dealer card
	   
	};
 	$.ajax({
			url: "/cardValue",
			type: 'GET',
@ -305,51 +277,13 @@ function choicePhase(){
			success: function(response){
				
				dealer = JSON.parse(response);

				alert('dealers first card is: '+dealer);
				imageObj.src = "static/graphics/deck/"+dealer+".png";
				//return dealer
			}
+		
});
	// called once all cards are dealt
	// cycle through players if any balck jacks update wallet accordingly set winner to true
	// ask players to make a choice playerChoices() if stand move on to next player
@ -359,39 +293,6 @@ var imageObj2 = new Image();
	clearInterval(interval_id);
	playerChoices()
}
 function playerChoices(){

	// put in function to cycle through players nby getting player list starting at player 1
@ -400,26 +301,17 @@ function playerChoices(){
	//let player choose hit or stand
	document.getElementById("hit").addEventListener("click",hit);
	document.getElementById("stand").addEventListener("click",stand);
 }
function stand(){
	// tell dealer not to give any more cards to the current player
	var noCard = document.createElement('AUDIO');
	//noCard.src = 'static/graphics/sounds/stand.mp3';
	//noCard.play();
+		$.ajax({
			url: "/stay",
			type: 'POST',
			data:{'number':z}
				});
}
function hit(){
	//add code to get value of card from python code and calculate new value
@ -430,9 +322,7 @@ function hit(){
			type: 'GET',
			success: function(response){
				var newCard= JSON.parse(response);
 				dealNewCard(newCard);
 			}
		});
}
@ -448,7 +338,6 @@ function dealNewCard(source){

	imageObj4.src = "static/graphics/deck/"+source+".png";
}
 function endgame(){

	$.ajax({
@ -458,29 +347,41 @@ function endgame(){
				var winner= response;
				alert(winner);

+				updateInfo(winner)
				}
 		});
}
function updateInfo(winner){
	if(winner=="You win!"){

		var paidtop = document.getElementById('paid');
		paidtop.innerHTML = "Paid: "+(betValue() *2);
		var wallettop = document.getElementById('wallet');
		wallettop.innerHTML = "Wallet: "+(prev_wallet + betValue()*2);
		prev_wallet += (betValue()*2);
		$.ajax({
			url: "/updatePlayerInfo",
			type: 'POST',
			data: {'paid':true,'amount':prev_wallet}
		});
	}else if (winner == "Draw!"){
		var paidtop = document.getElementById('paid');
		paidtop.innerHTML = "Paid: "+(betValue());
		var wallettop = document.getElementById('wallet');
		wallettop.innerHTML = "Wallet: "+(prev_wallet + betValue());
		prev_wallet += (betValue());

	}else if(winner == "endhand"){
		newHand();
	}else{
		var loser = document.createElement('AUDIO');
		//loser.src = 'static/graphics/sounds/loser.mp3';
		//loser.play();
	}
				if (z==4){
					newGame();
			}
}
function table(){

	//function to draw table layout
@ -547,6 +448,57 @@ function table(){
	context.lineWidth = 15;
	context.stroke();
}
function continueGame(){	
}
function newHand(){

	$.ajax({
		url: "/newHand",
		type: 'GET',
		success: function(response){
			alert(response);
		},
		error: function(error) {
			alert('error');
		}
	});
	//function to start new game and reset player variableS
	document.getElementById("bet").disabled=false;
	for(z=1;z<5;z++){
		var clearElem = document.getElementById("chip"+z);//player id in here
		clearElem.parentNode.removeChild(clearElem);
	}
	context.clearRect(0,0,1200,750);
	table();

	player1 = {
		card1x:565,
	  	card1y:20,
	  	card2x:580,
	  	card2y:20
	};

	player2 = {
	  	card1x:565,
	  	card1y:20,
	  	card2x:580,
	  	card2y:20
	};

	player3 = {
	  	card1x:565,
	  	card1y:20,
	  	card2x:580,
	  	card2y:20
	};

	player4 = {
	  	card1x:565,
	  	card1y:20,
	  	card2x:580,
	  	card2y:20
	};	
}
function newGame(){

	$.ajax({
@ -554,7 +506,6 @@ function newGame(){
		type: 'GET',
		success: function(response){
			alert(response);
 		},
		error: function(error) {
			alert('error');
@ -597,3 +548,129 @@ function newGame(){
	  	card2y:20
	};	
}
// everything from this point on is to draw the other players cards and bets and handvalues
function getDB(){
	$.ajax({
		url: "/gameinfo",
		type: 'GET',
		success: function(response){
			if(response['hand1']){
				drawOtherPlayersCards(1,response['hand1'],response['seatnum'])
				drawOtherPlayersCards(2,response['hand2'],response['seatnum'])
			}
			if(response['hand3']){
				drawOtherPlayersCards(3,response['hand3'],response['seatnum'])
			}
			if(response['bet']){
				makeChip(response['seatnum'],response['bet'])
			}
			if (response['stay']){
				showPlayerValue(response['seatnum'],response['handValue'])
			}
			
		},
		error: function(error) {
			console.log(error)	;	}
	});
}

function drawOtherPlayersCards(cardNum,cardName,seatNum){
	var imageObj = new Image();
 	imageObj.onload = function() {
 	
 	// from the ajax request take the players seat number,card name, card number eg is it the first,second or a hit card
 	//draw accordingly

 			//deal out the players first card
 			if (seatNum ==1 && cardNum==1){
 				context.drawImage(imageObj, player1.card1x, player1.card1y, 80, 129);	
 				imageObj.src= "static/graphics/deck/"+cardName+".png";
 			}
 			else if(seatNum==2 && cardNum==1){
 				context.drawImage(imageObj, player2.card1x, player2.card1y, 80, 129);
 				imageObj.src= "static/graphics/deck/"+cardName+".png";
 			}
 			else if(seatNum==3 &&cardNum==1){
	        	context.drawImage(imageObj, player3.card1x, player3.card1y, 80, 129);
	        	imageObj.src= "static/graphics/deck/"+cardName+".png";
 			}
 			else if(seatNum==4 && cardNum==1){
				context.drawImage(imageObj, player4.card1x, player4.card1y, 80, 129);
				imageObj.src= "static/graphics/deck/"+cardName+".png";
 			}

 			//deal out the players second card
 			else if (seatNum ==1 && cardNum==2){
 				context.drawImage(imageObj, player1.card2x, player1.card2y, 80, 129);
 				imageObj.src= "static/graphics/deck/"+cardName+".png";	
 			}
 			else if(seatNum==2 && cardNum==2){
 				context.drawImage(imageObj, player2.card2x, player2.card2y, 80, 129);
 				imageObj.src= "static/graphics/deck/"+cardName+".png";
 			}
 			else if(seatNum==3 &&cardNum==2){
	        	context.drawImage(imageObj, player3.card2x, player3.card2y, 80, 129);
	        	imageObj.src= "static/graphics/deck/"+cardName+".png";
 			}
 			else if(seatNum==4 && cardNum==2){
				context.drawImage(imageObj, player4.card2x, player4.card2y, 80, 129);
				imageObj.src= "static/graphics/deck/"+cardName+".png";
 			}

 			// deal out the hit card
 			else if (seatNum ==1 && cardNum==3){
 				context.drawImage(imageObj, player1.card2x, player1.card2y-15, 80, 129);	
 				imageObj.src= "static/graphics/deck/"+cardName+".png";
 			}
 			else if(seatNum==2 && cardNum==3){
 				context.drawImage(imageObj, player2.card2x, player2.card2y-15, 80, 129);
 				imageObj.src= "static/graphics/deck/"+cardName+".png";
 			}
 			else if(seatNum==3 &&cardNum==3){
	        	context.drawImage(imageObj, player3.card2x, player3.card2y-15, 80, 129);
	        	imageObj.src= "static/graphics/deck/"+cardName+".png";
 			}
 			else if(seatNum==4 && cardNum==3){
				context.drawImage(imageObj, player4.card2x, player4.card2y-15, 80, 129);
				imageObj.src= "static/graphics/deck/"+cardName+".png";
 			}
  	};
}
function makeChip(playerId,betVal){
	var chip = document.createElement("div");
	var bet=  document.createTextNode(betVal);
	chip.id="chip"+playerId;
	chip.className="chip";
	chip.appendChild(bet);
	document.getElementById("canvas-container").appendChild(chip);
	var chipS = document.createElement("AUDIO");
	//chipS.src = "static/graphics/sounds/chipsound.mp3"; 
	//chipS.play()
}
function showPlayerValue(seatNum,playerValue){
	context.font = "15px Comic Sans MS";
	context.fillStyle = 'white';
	if (seatnum == 1){
		context.fillText('Players Value is: '+playerValue,155,650);
	}
	if (seatnum == 2){
		context.fillText('Players Value is: '+playerValue,385,650);
	}
	if (seatnum == 3){
		context.fillText('Players Value is: '+playerValue,615,650);
	}
	if (seatnum == 4){
		context.fillText('Players Value is: '+playerValue,850,650);
	}
}
function dealersTurn(){
	$.ajax({
				url: "/dealerValue",
				type: 'GET',
				success: function(response){
					var dealerValue= JSON.parse(response);
					alert('dealers total is:  '+dealerValue);
					endgame();
				}
			});
}