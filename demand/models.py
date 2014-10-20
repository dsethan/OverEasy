from django.db import models

class Demand(models.Model):
	first = models.CharField(max_length=30)
	last = models.CharField(max_length=30)
	email = models.CharField(max_length=50)
	phone = models.CharField(max_length=30)
	address = models.CharField(max_length=200)