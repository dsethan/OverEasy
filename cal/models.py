from datetime import date, time, timedelta, datetime

from django.db import models
from django.utils import timezone

from restaurants.models import Restaurant
#from orders.models import Order

class Entry(models.Model):
	time = models.TimeField()
	date = models.DateField()
	available = models.IntegerField(default=2)
	demand = models.IntegerField(default=0)
	restaurant = models.ForeignKey(Restaurant)
	length = models.IntegerField(default=20)
	shutoff_hour = models.IntegerField(default=2)
	shutoff_min = models.IntegerField(default=0)

	def week_num(self):
		iso = self.date.isocalendar()
		return iso[1]

	def week_day(self):
		iso = self.date.isocalendar()
		return iso[2]

	def end_time(self):
		dt = datetime.combine(self.time, self.date)
		td = datetime.timedelta(minutes=length)
		end = dt + td
		return end

	def get_date_string(self):
		return self.date.strftime("%m/%d/%Y")

	def get_start_time_string(self):
		return self.time.strftime("%I:%M")

	def get_end_time_string(self):
		return self.end_time.strftime("%I:%M")

	def get_demand_ratio(self):
		return float(demand/available)
	'''
	def get_orders_for_entry(self):
		orders = []

		for o in Orders.objects.all():
			if (o.entry.id == self.id):
				orders.append(o)

		return orders
	'''

	def open_or_closed(self):
		today = datetime.date.today()
		date = datetime.date.today().date()
		shutoff_time = time(self.shutoff_hour,self.shutoff_min)
		today_shutoff_time = datetime.combine(date, five)
		dt = datetime.combine(self.date, self.time)

		if dt < today_shutoff_time:
			return True

		return False

	def get_num_orders_for_entry(self):
		num = 0

		for o in Orders.objects.all():
			if (o.entry.id == self.id):
				num = num + 1

		return num

	def __unicode__(self):
		return "Entry id:" + str(self.id)