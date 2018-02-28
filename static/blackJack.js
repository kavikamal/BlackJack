var data;

function startGame(){
    var coin=document.getElementById("playerCoin").value;
    console.log(coin);
    data= {"msg":"newgame","playerCoin":parseInt(coin),"bet":10};
    hitAgain();
}


function hitAgain(){
    
    fetch("http://localhost:5000/blackjack", { 
        headers: new Headers({
            'Content-Type': 'application/json'
          }),
          body:JSON.stringify(data),
          method: "POST",
    }).then((resp) => resp.json())
    .then (function(cards) {
        displayFunction(cards)
    });
  }
  
function hit(){
    data.msg="hit"  
    hitAgain();
  }  
function stand(){
    data.msg="stand"  
    hitAgain();
  }


function surrender(){
    data.msg="surrender"  
    hitAgain();
  }
function displayFunction(cards) {
    var message="";  
    var winCheck=0;
    data=cards;
    var destination = document.getElementById("mainDiv"); 
    if (cards.msg=="hit"){
        if (cards.playerCoin<10) {  
            message="No enough coins to hit again"
            document.getElementById("startGameButton").hidden=true;
            document.getElementById("standButton").hidden=false;
            document.getElementById("surrenderButton").hidden=true;
            data.msg="stand";
        }    
        else{    
            document.getElementById("startGameButton").hidden=true; 
            document.getElementById("hitButton").hidden=false;
            document.getElementById("standButton").hidden=false;
            document.getElementById("surrenderButton").hidden=true;
            message="Hit again?"
        } 
    }else if (cards.msg=="surrender") {  
        document.getElementById("startGameButton").hidden=true;
        document.getElementById("hitButton").hidden=false;
        document.getElementById("surrenderButton").hidden=false;
        document.getElementById("standButton").hidden=true;
    }
    else {
        winCheck=1;
        if (cards.msg=="player"){
            message="Player Won"
        }  
        else if (cards.msg=="dealer") {
            message="Dealer Won"
        }
        else if (cards.msg=="both"){
            message="Both Lost!!!"
        }
        data.msg="newgame";
        document.getElementById("startGameButton").value="Play Again?";
        document.getElementById("startGameButton").hidden=false;
        document.getElementById("hitButton").hidden=true;
        document.getElementById("standButton").hidden=true;
        document.getElementById("surrenderButton").hidden=true;
    }   
    destination.innerHTML="";
    var h = document.createElement("p")
    h.setAttribute("class","msgClass");
    h.textContent=message;
    destination.appendChild(h);

    document.getElementById("playerCoin").value=cards.playerCoin;
    
    h = document.createElement("h4")
    h.textContent="Player Cards"; 
    destination.appendChild(h);
    for (let i=0;i<cards.player.length;i++){  
        let newImageElement = document.createElement("img");
        newImageElement.src=getImageName(parseInt(cards.player[i]));
        newImageElement.setAttribute("class","imgClass");
        destination.appendChild(newImageElement);   
    }  
    h = document.createElement("h4")
    h.textContent="Dealer Card"; 
    destination.appendChild(h);  
    for (let i=0;i<cards.dealer.length;i++){     
        if ((i==cards.dealer.length-1)&&(winCheck==0)){
            let newImageElement = document.createElement("img");
            newImageElement.src="/static/"+"card_closed.png";
            newImageElement.setAttribute("class","imgClass");
            destination.appendChild(newImageElement);
        }
        else{    
            let newImageElement = document.createElement("img");
            newImageElement.src=getImageName(parseInt(cards.dealer[i]));
            newImageElement.setAttribute("class","imgClass");
            destination.appendChild(newImageElement);   
        }    
    }
}
    
function getImageName(cardNo)
    {
        if (cardNo>0 && cardNo<14)
           imageName="/static/"+cardNo+ "_of_spades.png";  
        else if (cardNo>13 && cardNo<27){
           cardNo=cardNo-13;
           imageName="/static/"+cardNo+ "_of_clubs.png" ;
        }
        else if (cardNo>26 && cardNo<40){
           cardNo=cardNo-26;
           imageName="/static/"+cardNo+ "_of_hearts.png";
        }    
        else if (cardNo>39 && cardNo<53){
           cardNo=cardNo-39;
           imageName="/static/"+cardNo+ "_of_diamonds.png";
        }   
        return imageName   
    }

  