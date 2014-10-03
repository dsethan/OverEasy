from django.db import models
from datetime import date, time, timedelta
from django.conf import settings

class Restaurant(models.Model):
	# Basic profile data for Restaurant object
	name = models.CharField(max_length=50)
	address1 = models.CharField(max_length=100)
	address2 = models.CharField(max_length=100)
	city = models.CharField(max_length=50)
	state = models.CharField(max_length=14, choices=settings.US_STATES)

	# Define a maximum delivery radius for this Restaurant (IN METERS)
	# Default value is a 1.5 mile radius around the restaurant
	max_radius = models.IntegerField(default=2414)

	def get_address_string(self):
		space = " "
		address1 = str(self.address1)
		address2 = str(self.address2)
		city = str(self.city)
		state = str(self.state)
		return address1 + space + address2 + space + city + space + state

	def __unicode__(self):
		return str(self.name)