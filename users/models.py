from django.db import models
from django.contrib.auth.models import User
from datetime import date, time, timedelta
from googlemaps import GoogleMaps
from restaurants.models import Restaurant
from django.conf import settings

class UserProfile(models.Model):
	# Basic profile data for UserProfile object
	user = models.OneToOneField(User)
	address = models.CharField(max_length=50)
	city = models.CharField(max_length=50)
	state = models.CharField(max_length=2, choices=settings.US_STATES)
	phone = models.CharField(max_length=12)

	# Restaurant this UserProfile is mapped to
	#restaurant = models.ForeignKey(Restaurant)

	def get_address_string(self):
		space = " "
		address = str(self.address)
		city = str(self.city)
		state = str(self.state)
		return address + space + city + space + state

	def dist_to_restaurant(self):
		api_key = settings.GOOGLE_MAPS
		gmaps = GoogleMaps(api_key)
		start = self.get_address_string
		stop = self.restaurant.get_address_string
		dirs = gmaps.directions(start, stop)
		dist = dirs['Directions']['Distance']['meters']
		dist_in_miles = float(dist*.000621371)
		return dist_in_miles

	def time_to_user_profile(self):
		api_key = settings.GOOGLE_MAPS
		gmaps = GoogleMaps(api_key)
		start = self.get_address_string
		stop = self.restaurant.get_address_string
		dirs = gmaps.directions(start, stop)
		time = dirs['Directions']['Duration']['seconds']
		return time

	def dist_to_restaurant_string(self):
		return str(self.dist_to_restaurant)

	def time_to_user_profile_string(self):
		time = self.time_to_user_profile
		mins = str(time/60)
		secs = str(time%60)
		return mins + ":" + secs

	def __unicode__(self):
		return self.user.username

class DriverProfile(models.Model):
	# Basic profile data for DriverProfile object
	user = models.OneToOneField(User)
	address = models.CharField(max_length=50)
	city = models.CharField(max_length=50)
	state = models.CharField(max_length=2, choices=settings.US_STATES)
	phone = models.CharField(max_length=12)

	# Restaurant this DriverProfile is mapped to
	restaurant = models.ForeignKey(Restaurant)

class StaffProfile(models.Model):
	# Basic profile data for StaffProfile object
	user = models.OneToOneField(User)
	address = models.CharField(max_length=50)
	city = models.CharField(max_length=50)
	state = models.CharField(max_length=2, choices=settings.US_STATES)
	phone = models.CharField(max_length=12)

	# Restaurant this StaffProfile is mapped to
	restaurant = models.ForeignKey(Restaurant)
