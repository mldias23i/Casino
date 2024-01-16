from django.db import models

class Bet(models.Model):
    clientId = models.CharField(max_length=255, null=True, blank=True)
    roundId = models.CharField(max_length=255)
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    transactionId = models.CharField(max_length=255)
    currency = models.CharField(max_length=10)
    timestamp = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Bet {self.transactionId} ({self.currency} {self.amount})"


class Win(models.Model):
    clientId = models.CharField(max_length=255)
    roundId = models.CharField(max_length=255)
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    transactionId = models.CharField(max_length=255)

    def __str__(self):
        return f"Win - Transaction ID: {self.transactionId}"


class Refund(models.Model):
    clientId = models.CharField(max_length=255)
    roundId = models.CharField(max_length=255)
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    transactionId = models.CharField(max_length=255)
    refundTransactionId = models.CharField(max_length=255)

    def __str__(self):
        return f"Refund - Transaction ID: {self.transactionId}"