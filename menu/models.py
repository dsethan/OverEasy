from django.db import models
from item.models import Item
from restaurants.models import Restaurant

class Menu(models.Model):
	description = models.CharField(max_length=20)
	restaurant = models.ForeignKey(Restaurant)

class MenuItemLink(models.Model):
	item = models.ForeignKey(Item)
	restaurant = models.ForeignKey(Restaurant)