#This class was created to show that I can separate the endpoint of Win, Refund, Bet, getGames and gameLaunch
#in multiple classes so that the code is more organized.
#If the code becomes more complex I can use an approach like this and all the endpoints are in the class
#that represents them
#In this case I only separate the endpoint of bet and let the others stay in views.py

import json
from django.http import JsonResponse
from django.http import JsonResponse
import json, hashlib
from .models import *
from django.views.decorators.csrf import csrf_exempt


#This are examples Url they should be replaced by the ones that returns the real value of the wallet of the client
#and the one that validates the token 
callback_url = "https://callback_url.com"
auth_service_url = "https://game-services-test..../provider_id/client:login"
#Don't have access to the secret key so I used this on has an example and this key should be kepted in an environmental variable for security reasons
secretKey = "53943735-9756-4b9d-8025-51e835ab8170"

class BetLogic:
    def process_bet(request):
        if request.method == "POST":
            #Getting data from the request
            data = json.loads(request.body.decode("utf-8"))
            hash = request.META.get("HTTP_HASH")
            token = data.get("token")
            roundId = data.get("roundId")
            amount = data.get("amount")
            transactionId = data.get("transactionId")
            currency = data.get("currency")

            #Checking if the hash is present it can be added another validation for this value
            if not hash:
                errorResponse = {
                    "errorCode": 4005,
                    "error": "Required header 'Hash' is not present"   
                }
                return JsonResponse(errorResponse, status=200)
            
            #Checking if the token is present, another validations can be done to the token
            if not token:
                return JsonResponse({"error": "Expired token"})
            
            #Calling function to calculate Hash
            hash = calculateHash(data, secretKey)

            #Calling function to retrieve information about the client
            data = client_data(f"{callback_url}/wallet", hash)
            #Getting client data
            clientData = json.loads(data.content)
            clientBalance = clientData.get("balance")
            clientId = clientData.get("clientId")
            clientCurrency = clientData.get("currency")

            #Checking the currency from the client with the currency that the bet is being made
            if clientCurrency != currency:
                return JsonResponse({"errorCode": 7003,
                                "error": "Currency mismatch exception"}, 
                                status=200)
            
            #Validating that the transactionId is unique
            if Bet.objects.filter(transactionId=transactionId).exists():
                return JsonResponse({"errorCode": 7005,
                                "error": "Transaction had already processed"}, 
                                status=200)
            
            #if Bet.objects.filter(roundId=roundId).exists():
            #   return JsonResponse({"errorCode": 7005,
            #                   "error": "Transaction had already processed"}, 
            #                  status=200)

            #Validating if the client has balance to make the bet
            if clientBalance >= amount:
                clientBalance = clientBalance - amount
            else:
                return JsonResponse({"errorCode": 7007,
                                "error": "Insufficient funds"}, 
                                status=200)
            
            #Bet model instance
            betInstance = Bet(
                clientId = clientId,
                roundId=roundId,
                amount=amount,
                transactionId=transactionId,
                currency=currency
            )

            #Save instance in database
            betInstance.save()

            return JsonResponse({
                "currency": currency,
                "balance": clientBalance,
                "clientId": clientId
                })
        else:
            return JsonResponse({"errorCode": 4003,
                                "error": "Method not allowed"}, 
                                status=200)
        
#This function should calculate the hash to be used on the headers of some requests
@csrf_exempt
def calculateHash(data, secretKey):
    #Formatting the data so that the hash is created correctly
    formatData = {
        "token": data["token"],
        "amount": data["amount"],
        "transactionId": data["transactionId"],
        "currency": data["currency"],
        "roundId": data["roundId"]
    }

    #String JSON order
    dataStr = json.dumps(formatData, sort_keys=True)
    hash = hashlib.sha256(dataStr.encode() + secretKey.encode()).hexdigest()

    return hash

#This function should return the information about the client
@csrf_exempt
def client_data(callback_url, hash):
    #This token could be retrieved from another service
    token = "test-PodXo2je61lenukvS6dscWs7kajQnB5F"
    requestData = {
        "token": token
    }

    #Converting json to a string
    requestJson = json.dumps(requestData)
    
    #Creating the headers for a request to a service that should return the information about the client
    headers = {
        "Content-Type": "application/json",
        "Hash": hash 
        #"9490E4A06F0E6ECECA6F884933085655C5F6ADCFA8909A181C18211883B6A40DCCD48441F807B6CFFE16916D36751D520714EB37D6BCF655CC2AD"
    }

    #This response data should be retrieved from a service but since I don't have access I am returning the data has an example
    response_data = {
        "currency": "USD",
        "balance": 99999,
        "clientId": "43-4312345"
    }

    return JsonResponse(response_data)