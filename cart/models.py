from django.db import models
from cal.models import Entry
from item.models import Item
from users.models import UserProfile

class Cart(models.Model):
	profile = models.ForeignKey(UserProfile)
	total = models.IntegerField(default=0)
	entry = models.ForeignKey(Entry)

class CartItem(models.Model):
	cart = models.ForeignKey(Cart)
	item = models.ForeignKey(Item)
	qty = models.IntegerField(default=1)