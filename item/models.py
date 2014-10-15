from django.db import models

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

	def __unicode__(self):
		return self.name


class ItemCategory(models.Model):
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

	item = models.ForeignKey(Item)
	category = models.CharField(max_length=3, choices=CATEGORIES)

	def __unicode__(self):
		return self.item + " " + self.category