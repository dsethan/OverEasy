import re

from django.template import RequestContext
from django.shortcuts import render_to_response, redirect
from django.conf import settings
from django.http import HttpResponse
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required

from users.models import UserProfile, DriverProfile, StaffProfile
from restaurants.models import Restaurant
from demand.models import Demand

from pygeocoder import Geocoder
from googlemaps import GoogleMaps

def user_reg(request):
	context = RequestContext(request)

	states = []

	for state in settings.US_STATES:
		states.append(state[1])

	return render_to_response(
		'register.html',
		{
		'states':states,
		},
		context)

def process_new_user(request):
	context = RequestContext(request)

	if request.method == 'POST':
		first = request.POST.get('first')
		last = request.POST.get('last')
		username = request.POST.get('username')
		password1 = request.POST.get('password1')
		password2 = request.POST.get('password2')
		address1 = request.POST.get('address1')
		address2 = request.POST.get('address2')
		city = request.POST.get('city')
		state = request.POST.get('state')
		phone = request.POST.get('phone')

		address_string = get_address_string(address1, address2, city, state)

		un = verify_username(username)
		pw = verify_password(password1, password2)
		addr = verify_address(address_string)
		num = verify_phone(phone)
		nom = verify_name(first, last)
		res = verify_restaurant(address_string)
		print un, pw, addr, num, nom, res

		if un[0] and pw[0] and addr[0] and num[0] and nom[0] and res[0]:
			success = store_user_data(un, pw, addr, num, nom, res, request)
			return success

		else:
			failure = gather_errors_for_template(first, last, username, address_string, phone, 
				un, pw, addr, num, nom, res, request)
			return failure
	
	return user_reg(request)

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

	return 0

def return_associated_profile_type(user):
	'''
	Input: a User object
	Output:	1 if this is a UserProfile
			2 if this is a DriverProfile
			3 if this is a StaffProfile
			0 if it is not any type of profile
	'''

	for up in UserProfile.objects.all():
		if up.user == user:
			return up

	for dp in DriverProfile.objects.all():
		if dp.user == user:
			return dp

	for sp in StaffProfile.objects.all():
		if sp.user == user:
			return sp

	return None

def user_login(request):
	context = RequestContext(request)
	user = request.user

	ptype = get_profile_type(user)

	if user.is_superuser:
		return redirect('/dashboard')

	if user.is_active:
		if ptype == 1:
			return redirect('/cal')
		if ptype == 2:
			return redirect('driver', user=user)
		if ptype == 3:
			return redirect('kitchen', user=user)

	if request.method == 'POST':
		un = request.POST['username']
		pw = request.POST['password']

		user = authenticate(username=un, password=pw)

		if user is not None:
			if user.is_active:
				login(request, user)
				return user_type_redirect_manager(user, request)

			else:
				return render_to_response(
					'account_disabled.html',
					{},
					context)

		else:
			error = "The details you supplied do not match our records. Please try again!"
			return render_to_response(
				'login.html',
				{
				'error':error,
				},
				context)

	return render_to_response(
		'login.html',
		{},
		context)

@login_required
def user_logout(request):
	context = RequestContext(request)
	user = request.User

	logout(request)

	return HttpResponseRedirect("/")

def user_type_redirect_manager(user, request):
	context = RequestContext(request)

	ptype = get_profile_type(user)
	print ptype

	if user.is_active:
		if ptype == 1:
			return redirect('/cal/')
		if ptype == 2:
			return redirect('driver')
		if ptype == 3:
			return redirect('kitchen')

	return redirect('user_login')

def gather_errors_for_template(first, last, username, address_string, phone,
	un, pw, addr, num, nom, res, request):
	context = RequestContext(request)

	un_errors = []
	pw_errors = []
	addr_errors = []
	num_errors = []
	nom_errors = []
	res_errors = []

	if not un[0]:
		un_errors.append(un[1])

	if not pw[0]:
		pw_errors.append(pw[1])

	if not addr[0]:
		addr_errors.append(addr[1])

	if not num[0]:
		num_errors.append(num[1])

	if not res[0]:
		demand = demand_instance_found(first, last, username, address_string, phone, request)
		return demand

	states = []

	for state in settings.US_STATES:
		states.append(state[1])

	return render_to_response(
		'register.html',
		{
		'un_errors':un_errors,
		'pw_errors':pw_errors,
		'addr_errors':addr_errors,
		'num_errors':num_errors,
		'res_errors':res_errors,
		'states':states,
		},
		context)

def demand_instance_found(first, last, username, address_string, phone, request):
	context = RequestContext(request)

	_demand = Demand(
		first=first,
		last=last,
		email=username,
		phone=phone,
		address=address_string
		)

	_demand.save()

	return render_to_response(
		"coming_soon.html",
		{},
		context)

def store_user_data(un, pw, addr, num, nom, res, request):
	context = RequestContext(request)

	username = un[1]
	password = pw[1]
	address = addr[1]
	city = addr[2]
	state = addr[3]
	phone = num[1]
	first = nom[1]
	last = nom[2]
	restaurant = res[1]

	_user = User(
		first_name=first,
		last_name=last,
		username=username)

	_user.set_password(password)

	_user.save()

	_user_profile = UserProfile(
		user=_user,
		address=address,
		city=city,
		state=state,
		phone=phone,
		restaurant=restaurant)

	_user_profile.save()

	return render_to_response(
		'welcome.html',
		{'user_profile':_user_profile},
		context)

def verify_restaurant(start):
	api_key = settings.GOOGLE_MAPS
	geo = GoogleMaps(api_key)

	for r in Restaurant.objects.all():
		end = r.get_address_string()
		dirs = geo.directions(start, end)
		dist = dirs['Directions']['Distance']['meters']

		if dist < r.max_radius:
			return (True, r)

	error = "Unfortunately, we are not yet delivering in your area."
	return (False, error)

def verify_name(first, last):
	if not (first > 0) and (last > 0):
		error = "You must provide both a first and last name."
		return (False, error)
	f = first.title()
	l = last.title()
	return (True, f, l)

def verify_phone(phone):
	if not re.match(r"^\(?([0-9]{3})\)?[-. ]?([0-9]{3})[-. ]?([0-9]{4})$", phone):
		error = "Please provide a valid phone number."
		return (False, error)
	return (True, phone)

def verify_address(address_string):
	geo = Geocoder()
	result = Geocoder.geocode(address_string)
	if not result.valid_address:
		error = "Please enter a valid address."
		return (False, error)
	split = str(result).split(",")
	addr = split[0]
	city = split[1]
	state = split[2]
	return (True, addr, city, state)

def verify_password(password1, password2):
	if password1 != password2:
		error = "Passwords do not match."
		return (False, error)
	if len(password1) < 7:
		error = "Passwords must be at least 6 characters in length."
		return (False, error)

	return (True, password1)

def verify_username(username):
	if not re.match(r"^[_a-z0-9-]+(\.[_a-z0-9-]+)*@[a-z0-9-]+(\.[a-z0-9-]+)*(\.[a-z]{2,4})$", username):
		error = "Please enter a valid email address."
		return (False, error)

	users = User.objects.all()
	for u in users:
		if u.username == username:
			error = "This email already has an account associated with it."
			return (False, error)

	return (True, username)

def get_address_string(address1, address2, city, state):
	space = " "
	comma = ", "
	if len(address2) > 0:
		return address1 + space + address2 + comma + city + comma + state

	return address1 + comma + city + comma + state