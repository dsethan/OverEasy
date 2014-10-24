from django.db import models
from cal.models import Entry
from item.models import Item
from users.models import UserProfile

class Cart(models.Model):
	profile = models.ForeignKey(UserProfile)
	total = models.IntegerField(default=0)
	entry = models.ForeignKey(Entry)
	cart_still_active = models.BooleanField(default=True)

	def __unicode__(self):
		profile = str(self.profile)
		entry = str(self.entry)
		return entry + profile

	def is_active(self):
		if self.entry.orders_still_open() and self.entry.open():
			return True
		return False

	def get_cart_items(self):
		items = CartItem.objects.filter(cart=self)
		return items

	def get_items(self):
		items = CartItem.objects.filter(cart=self)
		i = []

		for item in items:
			i.append(item.item)

		return i

	def get_item_names_and_quantities(self):
		items = CartItem.objects.filter(cart=self)
		
		list_items = []
		for i in items:
			list_items.append(i.item.name)

		names_and_quantities = {}
		for i in list_items:
			if i not in names_and_quantities.keys():
				names_and_quantities[i] = list_items.count(i)

		return names_and_quantities

	def get_items_and_quantities(self):
		items = CartItem.objects.filter(cart=self)

		list_items = []
		for i in items:
			list_items.append(i.item)

		items_to_return = {}
		for i in list_items:
			if i not in items_to_return.keys():
				items_to_return[i] = list_items.count(i)

		return items_to_return

	def get_total_price_of_cart(self):
		items = CartItem.objects.filter(cart=self)
		total = 0
		for i in items:
			total = total + i.item.price
		return total

	def view_order_total_in_usd(self):
		items = CartItem.objects.filter(cart=self)
		total = 0
		for i in items:
			total = total + i.item.price
		self_str = str(total)
		cents = self_str[-2:]
		dollars = self_str[:-2]
		return "$" + dollars + "." + cents

	def get_tax_for_cart_in_cents(self):
		total = self.get_total_price_of_cart()
		tax_raw = total * 7.5
		grand = (tax_raw) * .0001
		tax_rounded = round(grand, 2)
		return tax_rounded

	def get_tax_for_cart(self):
		total = self.get_total_price_of_cart()
		tax_raw = total * 7.5
		grand = (tax_raw) * .01
		tax_rounded = round(grand, 0)
		return tax_rounded

	def grand_total(self):
		subtotal = self.get_total_price_of_cart()
		tax = self.get_tax_for_cart()
		return subtotal + tax

	def get_grand_total_in_usd(self):
		total = self.grand_total()
		total = int(total)
		self_str = str(total)
		cents = self_str[-2:]
		dollars = self_str[:-2]
		return "$" + dollars + "." + cents

	def get_tax_for_cart_in_usd(self):
		total = self.get_tax_for_cart()
		total = int(total)
		self_str = str(total)
		cents = self_str[-2:]
		dollars = self_str[:-2]
		return "$" + dollars + "." + cents



class CartItem(models.Model):
	cart = models.ForeignKey(Cart)
	item = models.ForeignKey(Item)
	qty = models.IntegerField(default=1)