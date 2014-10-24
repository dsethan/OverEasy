from django.db import models
from django.contrib.auth.models import User


class Referral(models.Model):
	initiator = models.ForeignKey(User)
	target_email = models.CharField(max_length=50)
	code = models.CharField(max_length=15)
	active = models.BooleanField(default=True)
	percent_discount = models.IntegerField(default=0)
	dollar_discount = models.IntegerField(default=0)
	
