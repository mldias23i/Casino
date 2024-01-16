from django.http import JsonResponse
import json
from .models import *
from django.views.decorators.csrf import csrf_exempt
from .betLogic import BetLogic
from .utils import *

#This is an example Url - it should be replaced by the one that returns the real value of the wallet of the client
#In a production environment this should be replaced by a real server with a public domain
callback_url = "https://callback_url.com"
#Don't have access to the secret key so I used this on has an example and this key should be kepted in an environmental variable for security reasons
secretKey = "53943735-9756-4b9d-8025-51e835ab8170"

#This function should return all the games available for the client to play
@csrf_exempt
def get_games(request):
    #Check if authorization token is present
    authorizationToken = request.META.get("HTTP_AUTHORIZATION")
    #The authorizationToken should be validated, I am just validating if it exists
    if not authorizationToken:
        return JsonResponse({"errorCode": 7001,
                             "error": "Session validation failed"}, 
                            status=200)
    
    if not validate_token(authorizationToken):
        return JsonResponse({"errorCode": 7001,
                            "error": "Session validation failed"}, 
                            status=200)
        
    #The list of games can be retrieved by a database or a request to another provider, in this case I put the results
    #hardcoded because I understand that I don't have any place to retrieve this data
    games=[{
            "gameId": "777magic",
            "gameName": "777 magic slots",
            "gameTypeId": "slots",
            "demoGameAvailable": True,
            "jackpotAvailable": True,
            "freeSpinAvailable": True,
            "isDesktop": True,
            "isMobile": True
        },
        {
            "gameId": "roulette",
            "gameName": "American Roulette",
            "gameTypeId": "live",
            "demoGameAvailable": True,
            "jackpotAvailable": False,
            "freeSpinAvailable": False,
            "isDesktop": True,
            "isMobile": True
        }
    ]

    return JsonResponse({"gameList": games})


#This function should return the link for launching the game
@csrf_exempt
def game_launch(request):
    #Check if authorization token is present
    #The authorizationToken should be validated, I am just validating if it exists
    authorizationToken = request.META.get("HTTP_AUTHORIZATION")
    if not authorizationToken:
        return JsonResponse({"errorCode": 7001,
                             "error": "Session validation failed"}, 
                            status=200)
    
    if not validate_token(authorizationToken):
        return JsonResponse({"errorCode": 7001,
                            "error": "Session validation failed"}, 
                            status=200)    
    
    if request.method == "POST":
        #Getting the data from the request
        data = json.loads(request.body.decode("utf-8"))
        gameId = data.get("gameId")
        demo = data.get("demo")
        
        #Checking if it is present the value of demo and if it's a boolean
        if not isinstance(demo, bool):
            errorResponse = {
                "errorCode": 7015,
                "error": "Game launch error."   
            }
            return JsonResponse(errorResponse, status=200)
        
        #Validating if demo is true or not and returning the corresponding link for each value of demo
        if demo:
            # Add the fake balance amount
            fakeBalance = 100000 #This can be changed has needed
            #With parameters for gameId, for demo=true and for balance
            gameUrl = f"https://game-launch-link/gameLaunch?game={gameId}&demo=true&balance={fakeBalance}" 
        else:
            #With parameters for gameId and for demo=false
            gameUrl = f"https://game-launch-link/gameLaunch?game={gameId}&demo=false" 

#Note: The others parameters received by the request we can use to modified the link to launch the game
        
        return JsonResponse({"url": gameUrl})
    else:
        return JsonResponse({"errorCode": 4003,
                             "error": "Method not allowed"}, 
                             status=200)

@csrf_exempt    
def bet(request):
    if request.method == "POST":
        return BetLogic.process_bet(request)
    else:
        return JsonResponse({"errorCode": 4003,
                             "error": "Method not allowed"}, 
                             status=200)


#This function is to update the balance of a client wallet when exists a win   
@csrf_exempt
def win(request):
    if request.method == "POST":
        #Getting data from the request
        data = json.loads(request.body.decode("utf-8"))
        hash = request.META.get("HTTP_HASH")
        token = data.get("token")
        clientId = data.get("clientId")
        roundId = data.get("roundId")
        amount = data.get("amount")
        transactionId = data.get("transactionId")

        #Validating the hash
        if not hash:
            errorResponse = {
                "errorCode": 4005,
                "error": "Required header 'Hash' is not present"   
            }
            return JsonResponse(errorResponse, status=200)
        
        #Validating the token
        if not token:
            return JsonResponse({"error": "Expired token"})
        
        #Validating if the clientId that wins has a roundId on the Bet table, if not it means that the bet was not made so the clientId
        #can't win the amount
        #If it exists than I can keep the currency that was used on the bet
        bet = Bet.objects.filter(roundId=roundId, clientId = clientId).first()
        #If it exists keep the currency value if not returns an error
        if bet:
            currency = bet.currency
        else:
            errorResponse = {
                "errorCode": 7004,
                "error": "Game round wasn't previously created"   
            }
            return JsonResponse(errorResponse, status=200)
        
        data["currency"] = currency

        #The currency was retrieved so that it is possible for the hash to be created
        hash = calculateHash(data, secretKey)

        #Validating if the transactionId already exists because this value should be unique
        if Win.objects.filter(transactionId=transactionId).exists():
            return JsonResponse({"errorCode": 7005,
                             "error": "Transaction had already processed"}, 
                             status=200)

        #Win model instance
        winInstance = Win(
            clientId=clientId,
            roundId=roundId,
            amount=amount,
            transactionId=transactionId,
        )

        #Save instance in database
        winInstance.save()

        #Getting information about the client
        data = client_data(f"{callback_url}/wallet", hash)
        clientData = json.loads(data.content)
        clientBalance = clientData.get("balance")
        clientId = clientData.get("clientId")
        clientCurrency = clientData.get("currency")
        #Updating the balance of the client
        clientBalance = clientBalance + amount
        return JsonResponse({
                "currency": clientCurrency,
                "balance": clientBalance,
                "clientId": clientId
                })
    else:
        return JsonResponse({
            "errorCode": 4003,
            "error": "Method not allowed"
            }, status=200)

#This function refunds the client when a problem occurs or when the client decides to cancel a bet
@csrf_exempt
def refund(request):
    if request.method == "POST":
        #Getting data from the request
        data = json.loads(request.body.decode("utf-8"))
        token = data.get("token")
        clientId = data.get("clientId")
        roundId = data.get("roundId")
        amount = data.get("amount")
        transactionId = data.get("transactionId")
        refundTransactionId = data.get("refundTransactionId")

        #Validating the token
        if not token:
            return JsonResponse({"error": "Expired token"})

        #Checking if the Bet table has a roundId equal to the one that is being used in the request of the refund
        #Only need one that is equal so that I can retrieve the currency in which the bet was made
        bet = Bet.objects.filter(roundId=roundId).first()
        
        #If it exists keep the currency value if not returns an error
        if bet:
            currency = bet.currency
        else:
            errorResponse = {
                "errorCode": 7004,
                "error": "Game round wasn't previously created"   
            }
            return JsonResponse(errorResponse, status=200)
        
        data["currency"] = currency
                
        #The currency was retrieved so that it is possible for the hash to be created
        hash = calculateHash(data, secretKey)

        #Validating if the transactionId exists on the bet table
        if not Bet.objects.filter(transactionId = transactionId).exists():
            return JsonResponse({"errorCode": 7006,
                             "error": "Bet transaction not found"}, 
                             status=200)

        #Validating if a game error occurred or if the client cancel the bet, if this does not happened the refund should not be possible
        if gameError(roundId) == False and cancelBet(transactionId) == False:
             return JsonResponse({"errorCode": 7006,
                             "error": "Bet transaction not found"}, 
                             status=200)
        
        #Refund model instance
        refundInstance = Refund(
            clientId=clientId,
            roundId=roundId,
            amount=amount,
            transactionId=transactionId,
            refundTransactionId = refundTransactionId
        )

        #Save instance in database
        refundInstance.save()
        
        #Getting information about the client
        data = client_data(f"{callback_url}/wallet", hash)
        clientData = json.loads(data.content)
        clientBalance = clientData.get("balance")
        clientCurrency = clientData.get("currency")
        
        #Updating the balance of the client
        clientBalance = clientBalance + amount

        return JsonResponse({
                "currency": clientCurrency,
                "balance": clientBalance,
                "clientId": clientId
                })
    else:
        return JsonResponse({
            "errorCode": 4003,
            "error": "Method not allowed"
            }, status=200)