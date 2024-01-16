import json, hashlib, requests 
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt

#This is the URL that returns the token
#It should be replaced by the actual URL that returns the token so that the call to the service is established
auth_service_url = "https://game-services-test..../provider_id/client:login"

#This data is to be used in getToken function
#This data should be obtained by a database or a call to another service 
client_id = "1-981242882"
password = "kiJS3trfFo9L"
provider_id = "provider_id"


#This function should calculate the hash to be used on the headers of some requests
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
def client_data(callback_url, hash):
    #Function to obtain token
    #token = getToken(client_id, password, provider_id)
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

    #This is an example of what it is possible to be done to retrieve info of a client from a service
    #try:
    #    response = requests.post(callback_url, data=requestJson, headers=headers)

    #    if response.status_code == 200:
    #        responseData = response.json()
    #        return responseData
    #    else:
    #        print(f"Error: {response.status_code}")
    #        return None
        
    #except Exception as e:
    #    print(f"Error: The request failed to obtain data")
    #    return None

#This function should call for a service that validates the token
def validate_token(token):
    return True

#This should validate if a game error occurred so that the refund is possible
#I don't have access to this information so I return a hardcoded value
def gameError(roundId):
    return True

#This should validate if a bet was canceled so that the refund is possible
#I don't have access to this information so I return a hardcoded value
def cancelBet(transactionId):
    return True

#This should retrieve a valid token to be used to get information as the data of the client from the wallet
#It should be used a valid auth_service_url
@csrf_exempt    
def getToken(client_id, password, provider_id):

    headers = {
        'Content-Type': 'application/json'
    }

    data = {
        "clientId": client_id,
        "password": password
    }

    response = requests.post(auth_service_url, json=data, headers=headers)

    if response.status_code == 200:
        response_data = response.json()
        token = response_data.get("token")
        return token
    else:
        return JsonResponse({"error": "Information not valid!"})