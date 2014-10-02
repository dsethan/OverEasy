from django.shortcuts import render
from users.models import UserProfile, DriverProfile, StaffProfile
from django.contrib.auth.models import User
from datetime import date, time, timedelta
from pygeocoder import Geocoder
from googlemaps import GoogleMaps
from restaurants.models import Restaurant
from django.conf import settings



def get_profile_type(user):
	'''
	Input: a User object
	Output:	1 if this is a UserProfile
			2 if this is a DriverProfile
			3 if this is a StaffProfile
			0 if it is not any type of profile
	'''

	for up in UserProfile.objects.all():
		if up.user == user:
			return 1

	for dp in DriverProfile.objects.all():
		if dp.user == user:
			return 2

	for sp in StaffProfile.objects.all():
		if sp.user == user:
			return 3

	return 4

def user_profile_register(request):
	context = RequestContext(request)

	if request.method == 'POST':
		email = request.POST.get('email')
		password1 = request.POST.get('password1')
		password2 = request.POST.get('password2')
		address1 = request.POST.get('address1')
		address2 = request.POST.get('address2')
		city = request.POST.get('city')
		state = request.POST.get('state')
		phone = request.POST.get('phone')

		v_email = validate_email(email)
		v_password = validate_password(password1, password2)
		v_address = validate_address(address1, address2, city, state)
		v_phone = validate_phone(phone)

		if v_email and v_password and v_address and v_phone:
			c_address = clean_address(address1, address2, city, state)
			c_phone = clean_phone(phone)


def clean_address(address1, address2, city, state):
	address_string = get_address_string(address1, address2, city, state)
	geo = Geocoder()
	result = Geocoder.geocode(address_string)
	return result

def validate_email(email):
	if not re.match(r"^[_a-z0-9-]+(\.[_a-z0-9-]+)*@[a-z0-9-]+(\.[a-z0-9-]+)*(\.[a-z]{2,4})$", email):
		return "Please provide a valid email address."
	return True

def validate_password(password1, password2):
	if len(password1) < 6:
		return "Passwords must be at least 6 characters long."
	if password1 != password2:
		return "Passwords do not match."
	return True

def validate_address(address1, address2, city, state):
	address_string = get_address_string(address1, address2, city, state)
	geo = Geocoder()
	is_valid = g.geocode(address_string).valid_address
	if not is_valid:
		return "Please provide a valid address."

	return True

def validate_phone(phone):
	if not re.match(r"^\(?([0-9]{3})\)?[-. ]?([0-9]{3})[-. ]?([0-9]{4})$", phone):
		return "Please provide a valid phone number, including area code."
	return True

def get_address_string(address1, address2, city, state):
	space = " "
	comma = ", "
	return address1 + space + address2 + comma + city + comma + state


def find_restaurant(address_string):
	api_key = settings.GOOGLE_MAPS
	geo = GoogleMaps(api_key)
	start = address_string

	for restaurant in Restaurant.objects.all():
		end = restaurant.get_address_string
		dirs = geo.directions(start, end)
		dist = dirs['Directions']['Distance']['Meters']

		if dist < restaurant.max_radius:
			return restaurant

	return "Sorry, you are not within a valid delivery area."

