from flask import Flask, render_template, jsonify, request
from random import choice as rc
import sys
import itertools 
import json
from flask_cors import CORS

app = Flask(__name__)
CORS(app)
cards=list(range(1,52)) 

@app.route("/",methods = ['GET'])
def firstPage():
    return render_template("index.html")

@app.route('/blackjack', methods = ['POST', 'GET'])
def result():
    playerTotal=0
    dealerTotal=0
    cards=list(range(1,52))
    if request.method == 'POST':
        recievedMsg=request.json["msg"]
        
        if  recievedMsg == 'newgame':
            player=[]
            dealer=[]
            data={}
            playerCoin=request.json["playerCoin"]
            bet=10
            player.append(rc(cards))
            cards.remove(player[0])
            player.append(rc(cards))
            cards.remove(player[1])
            playerTotal=getTotalCardValue(player)
            if playerTotal<21:
            #Dealer Hand
                dealer.append(rc(cards))
                cards.remove(dealer[0])
                dealer.append(rc(cards))
                cards.remove(dealer[1])
                dealerTotal=getTotalCardValue(dealer)
                if dealerTotal>21:
                    #If dealers total is greater than 21 select cards again 
                    cards.append(dealer[0])
                    cards.append(dealer[1])
                    dealer[0]= rc(cards)
                    cards.remove(dealer[0])
                    dealer[1]= rc(cards)
        else:
            dealer=request.json["dealer"]
            player=request.json["player"]
            playerCoin=request.json["playerCoin"]
            bet=request.json["bet"]
            cards = [x for x in cards if x not in player]
            cards = [x for x in cards if x not in dealer]
 
        if (playerCoin>=10 and recievedMsg in {'hit','newgame'}): 
                playerCoin=playerCoin-10  
                bet=bet+10
               
        if recievedMsg=="hit":
            player.append(rc(cards))
            cards.remove(player[len(player)-1])
            dealer.append(rc(cards))
            cards.remove(dealer[len(dealer)-1])
        elif recievedMsg=="surrender":
            dealerTotal=getTotalCardValue(dealer)
            while dealerTotal<17:
                tmpCard=rc(cards)
                tmpdealerTotal=dealerTotal+getCardValue(tmpCard)
                if tmpdealerTotal<17:
                   cards.remove(tmpCard) 
                   dealer.append(tmpCard)
                   dealerTotal=tmpdealerTotal
                else:
                    break   
        elif recievedMsg=="stand":
            dealerTotal=getTotalCardValue(dealer)
            playerTotal=getTotalCardValue(player)
            if playerTotal<dealerTotal:
                    msg="dealer"  
            else:
                    msg="player"  
                    playerCoin += 2*bet

        dealerTotal=getTotalCardValue(dealer)
        playerTotal=getTotalCardValue(player)
        
        if playerTotal>21:
            if dealerTotal<=21:
               msg="dealer"
            else: 
               msg="both"    
        elif playerTotal==21:
            msg="player"
            playerCoin += 2*bet
        elif playerTotal<21:
            if dealerTotal>21:
                msg="player"
            elif dealerTotal<21:    
                if recievedMsg=='newgame':
                    msg="surrender"
                elif recievedMsg=='surrender':  
                    if playerTotal<dealerTotal:
                        msg="dealer"  
                        playerCoin=playerCoin+ 5
                    else:
                        msg="player" 
                        playerCoin += 2*bet
                else:
                    msg="hit"

    data={"player":player,"dealer":dealer,"msg":msg,"playerCoin":playerCoin,"bet":bet} 
    return jsonify(data)

def getCardValue(cardNo):
    if cardNo>13 and cardNo<27:
           cardNo=cardNo-13
    elif cardNo>26 and cardNo<40:
           cardNo=cardNo-26
    elif cardNo>39 and cardNo<53:
           cardNo=cardNo-39
    return cardNo      

def getTotalCardValue(cards):
    acesCount=0
    total=0
    for i in cards:
        tmpCardValue=getCardValue(int(i))
        if (tmpCardValue==1):
            acesCount+=1
            total=total+11
        elif (tmpCardValue>10):
            total=total+10
        else:
            total=total+tmpCardValue
    for x in range(acesCount):  
        if total>21:
            total-=10   
    return total
            
if __name__ == "__main__":
    app.run(debug=True,threaded=True)