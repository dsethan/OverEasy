from django.db import models
from django.conf import settings

class Item(models.Model):
	HOT = 'HOT'
	DRINK = 'BEV'
	COLD = 'COLD'
	PRE = 'PRE'
	PREP_CATEGORIES = (
		(HOT, 'HOT'),
		(COLD, 'COLD'),
		(PRE, 'PRE'),
		(DRINK, 'BEV')
		)

	CLASSIC = 'CLA'
	JUICE = 'JUI'
	SIDES = 'SID'
	DRINKS = 'DRI'

	CATEGORIES = (
		(CLASSIC, 'CLA'),
		(JUICE, 'JUI'),
		(SIDES, 'SID'),
		(DRINKS, 'DRI'),
		)


	name = models.CharField(max_length=50)
	price = models.IntegerField(default=0) # in cents
	cost = models.IntegerField(default=0) # in cents
	description = models.TextField(max_length=10)
	prep_category = models.CharField(max_length=5,choices=PREP_CATEGORIES)
	number_ordered = models.IntegerField(default=0)
	total_spent = models.IntegerField(default=0)
	available = models.BooleanField(default=False)

	def format_price_usd(self):
		if len(self.price) == 2:
			return "$" + "0." + str(self.price)
		if len(self.price) > 2:
			price_string = str(self.price)
			return "$" + price_string[0:len(price_string)-2] + "." + price_string[len(price_string)-2:len(price_string)]

		return "issue"

	def view_price_usd(self):
		self_str = str(self.price)
		cents = self_str[-2:]
		dollars = self_str[:-2]
		return "$" + dollars + "." + cents

	def name_in_caps(self):
		return self.name.upper()

	def __unicode__(self):
		return self.name


class ItemCategory(models.Model):
	item = models.ForeignKey(Item)
	category = models.CharField(max_length=3, choices=settings.ITEM_CATEGORIES)

	def __unicode__(self):
		return self.item.name + " " + self.category