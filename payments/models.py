from django.db import models
from django.contrib.auth.models import User

class Card(models.Model):
	user = models.ForeignKey(User)
	customer = models.CharField(max_length=30)
	token = models.CharField(max_length=30)

class CardData(models.Model):
	DISCOVER = 'DIS'
	VISA = 'VIS'
	AMEX = 'AME'
	MASTERCARD = 'MCD'
	CARD_TYPES = (
		(DISCOVER, 'DIS'),
		(VISA, 'VIS'),
		(AMEX, 'AME'),
		(MASTERCARD, 'MCD')
		)
	card = models.ForeignKey(Card)
	company = models.CharField(max_length=15,choices=CARD_TYPES)
	last_four = models.CharField(max_length=5, default="****")	