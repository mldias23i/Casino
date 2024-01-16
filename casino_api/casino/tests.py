from django.test import TestCase
from django.urls import reverse
from .models import Bet, Win, Refund
import json

class BetTest(TestCase):
    def test_bet(self):
        data = {
            "token": "test-jYPqoviUriiubZdha5S)BevwvRK4rktb",
            "roundId": "4d206dd2-2d15-4f03",
            "amount": 100,
            "transactionId": "417b6958-b746",
            "currency": "USD"
            }
        data_json = json.dumps(data)  
        response = self.client.post(
            reverse('bet'), 
            data=data_json,  
            content_type='application/json', 
            HTTP_HASH='2DA0E4A06F0E6ECECA6F884933085655C5F6ADCFA8909A181C18211883B6A40DCCD48441F807B6CFFE16916D36751D520714EB37D6BCF655CC2AD'
        )

        self.assertEqual(response.status_code, 200)

        self.assertTrue(Bet.objects.filter(transactionId='417b6958-b746').exists())


class WinTest(TestCase):
    def test_win(self):
        Bet.objects.create(
                    clientId="43-12345",
                    roundId="4d206dd2-2d15-4f03",
                    amount=100,
                    transactionId="dc5fbe6f-abbe",
                    currency="USD"
                )
        
        data = {
                "token": "test-jYPqgoviUriiubZdha5Sc)BevwvRK4rktb",
                "clientId": "43-12345",
                "roundId": "4d206dd2-2d15-4f03",
                "amount": 100,
                "transactionId": "dc5fbe6f-abbe"
                }
        data_json = json.dumps(data)  
        response = self.client.post(
            reverse('win'), 
            data=data_json,  
            content_type='application/json', 
            HTTP_HASH='2DA0E4A06F0E6ECECA6F884933085655C5F6ADCFA8909A181C18211883B6A40DCCD48441F807B6CFFE16916D36751D520714EB37D6BCF655CC2AD'
        )

        self.assertEqual(response.status_code, 200)
        self.assertTrue(Win.objects.filter(transactionId='dc5fbe6f-abbe').exists())


class RefundTest(TestCase):
    def test_refund(self):
        bet = Bet.objects.create(
            clientId="43-12345",
            roundId="4d296dd2-2d15-4f03",
            amount=100,
            transactionId="dc5fbe6f-abbe",
            currency="USD"
        )
        data = {
            "token": "test-jYPqgoviUriiubZdha5Sc)BevwvRK4rktb",
            "clientId": "43-12345",
            "roundId": "4d296dd2-2d15-4f03",
            "amount": 50, 
            "transactionId": "dc5fbe6f-abbe", 
            "refundTransactionId": "dc5fbe6f-refund"
        }
        data_json = json.dumps(data)
        response = self.client.post(
            reverse('refund'),
            data=data_json,
            content_type='application/json',
            HTTP_HASH='2DA0E4A06F0E6ECECA6F884933085655C5F6ADCFA8909A181C18211883B6A40DCCD48441F807B6CFFE16916D36751D520714EB37D6BCF655CC2AD'
        )

        self.assertEqual(response.status_code, 200)
        self.assertTrue(Refund.objects.filter(transactionId='dc5fbe6f-abbe').exists())
