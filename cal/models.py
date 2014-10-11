from datetime import date, time, timedelta, datetime

from django.db import models
from django.utils import timezone

from restaurants.models import Restaurant
#from orders.models import Order

class Entry(models.Model):
	time = models.TimeField()
	date = models.DateField()
	original_capacity = models.IntegerField(default=2)
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
		dt = datetime.combine(self.date, self.time)
		td = timedelta(minutes=self.length)
		end = dt + td
		return end

	def get_date_string(self):
		return self.date.strftime("%m/%d/%Y")

	def get_start_time_string(self):
		return self.time.strftime("%I:%M")

	def get_end_time_string(self):
		end =  self.end_time()
		return end.strftime("%I:%M")

	def get_demand_ratio(self):
		return float(demand/original_capacity)
	'''
	def get_orders_for_entry(self):
		orders = []

		for o in Orders.objects.all():
			if (o.entry.id == self.id):
				orders.append(o)

		return orders
	'''
	def orders_still_open(self):
		if self.available == 0:
			return False
		else:
			return True

	def open(self):
		today = datetime.today()
		today_date = today.date()
		today_time = today.time()
		shutoff_time = time(self.shutoff_hour,self.shutoff_min)
		entry_shutoff_time = datetime.combine(self.date, shutoff_time)
		dt = datetime.combine(today_date, today_time)

		if dt < entry_shutoff_time:
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