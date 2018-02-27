var data;
function startGame(){
    fetch("http://localhost:5000/blackJack")
        .then((resp) => resp.json())
        .then(function(cards) {
             displayFunction(cards);
    });
}

function hitAgain(){
    fetch("http://localhost:5000/hit", { 
        headers: new Headers({
            'Content-Type': 'application/json'
          }),
          body:JSON.stringify(data),
          method: "POST",
    }).then((resp) => resp.json())
    .then (function(cards) {
        //alert(cards)
        displayFunction(cards)
    });
  }

  function surrender(){
    data.msg="surrender"  
    hitAgain();
  }

  function displayFunction(cards) {
    var msg="";  
    var winCheck=0;
    data=cards;
    var destination = document.getElementById("mainDiv"); 
    if (cards.msg=="play"){
       if (cards.playerCoin>10) {
        document.getElementById("buttonDiv1").hidden=false;   
        msg="Hit again?"
       }else{
        msg="No enough coins to hit again"
        document.getElementById("buttonDiv1").hidden=true;
        data.msg="surrender";
       }
        document.getElementById("buttonDiv2").hidden=true;
       document.getElementById("buttonDiv3").hidden=false;
    }else {
        winCheck=1;
        if (cards.msg=="player"){
          msg="Player Won"
        }  
        else if (cards.msg=="computer") {
            msg="Dealer Won"
        }
        data.msg="newgame";
        data.bet=10;
        document.getElementById("hitButton").value="Play Again?";
        document.getElementById("buttonDiv1").hidden=true;
        document.getElementById("buttonDiv2").hidden=false;
        document.getElementById("buttonDiv3").hidden=true;
    }   
    var count = Object.keys(cards).length;
    destination.innerHTML="";
    var h = document.createElement("p")
    var t = document.createTextNode(msg); 
    var c=document.getElementById("playerCoin");
    c.value=cards.playerCoin;
    h.appendChild(t); 
    destination.appendChild(h);
    document.getElementById("buttonDiv1").hidden=false;
    document.getElementById("buttonDiv2").hidden=true;
    document.getElementById("buttonDiv3").hidden=false;
    h = document.createElement("h4")
    t = document.createTextNode("Player Cards"); 
    h.appendChild(t);
    destination.appendChild(h);

    for (let i=0;i<cards.player.length;i++){  
        let newImageElement = document.createElement("img");
        newImageElement.src=getImageName(parseInt(cards.player[i]));
        newImageElement.setAttribute("class","imgClass");
        destination.appendChild(newImageElement);   
    }  
    h = document.createElement("h4")
    t = document.createTextNode("Dealer Card"); 
    h.appendChild(t);
    destination.appendChild(h);  
    for (let i=0;i<cards.computer.length;i++){     
        if ((i==cards.computer.length-1)&&(winCheck==0)){
            let newImageElement = document.createElement("img");
            newImageElement.src="/static/"+"card_closed.png";
            newImageElement.setAttribute("class","imgClass");
            destination.appendChild(newImageElement);
        }
        else{    
            let newImageElement = document.createElement("img");
            newImageElement.src=getImageName(parseInt(cards.computer[i]));
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

  