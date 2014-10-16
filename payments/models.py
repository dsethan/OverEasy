from django.db import models
from django.contrib.auth.models import User

class Card(models.Model):
	user = models.ForeignKey(User)
	customer = models.CharField(max_length=30)
	token = models.CharField(max_length=30)