from django.db import models

class Demand(models.Model):
	first = models.CharField(max_length=30)
	last = models.CharField(max_length=30)
	email = models.CharField(max_length=30)
	phone = models.IntegerField(max_length=12)
	address = models.CharField(max_length=200)