from flask import Flask, render_template, jsonify, request
from random import choice as rc
import sys
import itertools 
import json
from flask_cors import CORS
import requests

app = Flask(__name__)
CORS(app)
cards=list(range(1,52)) 

@app.route("/",methods = ['GET'])
def firstPage():
    return render_template("index.html")
 

@app.route('/blackjack', methods = ['POST', 'GET'])
def result():
    playerTotal=0
    computerTotal=0
    cards=list(range(1,52))
    #print(request.json["msg"])
    if request.method == 'POST':
        recievedMsg=request.json["msg"]
        if  recievedMsg == 'newgame':
            player=[]
            computer=[]
            data={}
            playerCoin=request.json["playerCoin"]
            bet=10
            player.append(rc(cards))
            cards.remove(player[0])
            player.append(rc(cards))
            cards.remove(player[1])
            playerTotal=getTotalCardValue(player)
            if playerTotal<21:
            #Computer Hand
                computer.append(rc(cards))
                cards.remove(computer[0])
                computer.append(rc(cards))
                cards.remove(computer[1])
                computerTotal=getTotalCardValue(computer)
                if computerTotal>21:
                    #If computers total is greater than 21 select cards again 
                    cards.append(computer[0])
                    cards.append(computer[1])
                    computer[0]= rc(cards)
                    cards.remove(computer[0])
                    computer[1]= rc(cards)
        else:
            computer=request.json["computer"]
            player=request.json["player"]
            playerCoin=request.json["playerCoin"]
            bet=request.json["bet"]
            cards = [x for x in cards if x not in computer]
            cards = [x for x in cards if x not in player]
        if (playerCoin>=10 and recievedMsg in {'hit','newgame'}): 
                playerCoin=playerCoin-10  
                bet=bet+10
               
        if recievedMsg=='hit':
            player.append(rc(cards))
            cards.remove(player[len(player)-1])
            computer.append(rc(cards))
            cards.remove(computer[len(computer)-1])
        elif recievedMsg=="surrender":
            computerTotal=getTotalCardValue(computer)
            while computerTotal<17:
                computer.append(rc(cards))
                computerTotal=getTotalCardValue(computer)
                if computerTotal<17:
                   cards.remove(computer[len(computer)-1]) 
        elif recievedMsg=="stand":
            computerTotal=getTotalCardValue(computer)
            playerTotal=getTotalCardValue(player)
            if playerTotal<computerTotal:
                    msg="computer"  
            else:
                    msg="player"  
                    playerCoin += 2*bet
        computerTotal=getTotalCardValue(computer)
        playerTotal=getTotalCardValue(player)
        if playerTotal>21:
            msg="computer"
        elif playerTotal==21:
            msg="player"
            playerCoin += 2*bet
        elif playerTotal<21:
            if recievedMsg=='newgame':
                msg="surrender"
            elif recievedMsg=='surrender':  
                if playerTotal<computerTotal:
                    msg="computer"  
                    playerCoin=playerCoin+ 5
                else:
                    msg="player" 
                    playerCoin += 2*bet
    data={"player":player,"computer":computer,"msg":msg,"playerCoin":playerCoin,"bet":bet} 
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