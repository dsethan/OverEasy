from django.db import models
from users.models import UserProfile
from cal.models import Entry
from item.models import Item
from datetime import datetime, date, time, timedelta

class Order(models.Model):
	PENDING = 'PDG'
	DELIVERY = 'OUT'
	DELIVERED = 'DVD'
	DATE = date(2000, 1, 1)
	TIME = time(12, 00)
	DATE_NOW = date.today()
	TIME_NOW = datetime.now().time()

	STATUS = (
		(PENDING, 'PDG'),
		(DELIVERY, 'OUT'),
		(DELIVERED, 'DVD'),
		)

	profile = models.ForeignKey(UserProfile)
	total = models.IntegerField(default=0)
	entry = models.ForeignKey(Entry)

	date_placed = models.DateField(auto_now_add=True)
	time_placed = models.TimeField(auto_now_add=True)

	date_delivered = models.DateField(auto_now=False, default=DATE)
	time_delivered = models.TimeField(auto_now=False, default=TIME)

	status = models.CharField(max_length=3, choices=STATUS, default=PENDING)

	order_rating = models.IntegerField(default=0)

	def __unicode__(self):
		return self.status

	def view_order_total_in_usd(self):
		self_str = str(self.total)
		cents = self_str[-2:]
		dollars = self_str[:-2]
		return "$" + dollars + "." + cents

	def get_all_items_for_order(self):
		return OrderItem.objects.filter(order=self)

	def get_all_item_names_for_order(self):
		ors = []
		for o in OrderItem.objects.filter(order=self):
			str_to_return = str(o.item.name) + " Qty: " + str(o.quantity)
			ors.append(str_to_return)
		return ors

	def get_all_item_names_for_order_with_category(self):
		ors = []
		for o in OrderItem.objects.filter(order=self):
			str_to_return = str(o.item.name) + " Qty: " + str(o.quantity)
			ors.append((str_to_return, o.item.prep_category))
		return ors


class OrderItem(models.Model):
	item = models.ForeignKey(Item)
	order = models.ForeignKey(Order)
	quantity = models.IntegerField(default=0)