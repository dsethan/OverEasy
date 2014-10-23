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

class CardAttributes(models.Model):
	card = models.ForeignKey(Card)
	brand = models.CharField(max_length=30)
	exp_month = models.CharField(max_length=2)
	exp_year = models.CharField(max_length=4)
	last_four = models.CharField(max_length=4)

	def get_expiration_string(self):
		month = str(self.exp_month)
		year = str(self.exp_year)
		return month + "/" + year