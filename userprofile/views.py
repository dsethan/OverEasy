import re
import random

from django.template import RequestContext
from django.shortcuts import render_to_response, redirect
from django.conf import settings
from django.http import HttpResponse
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required

from users.models import UserProfile
from orders.models import Order, OrderItem
from promotion.models import Referral

from twilio.rest import TwilioRestClient

@login_required
def display_profile(request):
	context = RequestContext(request)
	user = request.user
	profile = UserProfile.objects.get(user=user)
	orders = Order.objects.filter(profile=profile)

	no_orders_yet = False

	if len(orders) == 0:
		no_orders_yet = True

	referral = None

	for r in Referral.objects.all():
		if r.profile == profile:
			referral = r

	if referral == None:
		new_referral = Referral(
			profile=profile,
			referral_code=generate_referral_code(),
			)

		new_referral.save()
		referral = new_referral

	return render_to_response(
		'profile.html',
		{
		'profile':profile,
		'orders':orders,
		'no_orders_yet':no_orders_yet,
		'referral':referral,
		},
		context)

def generate_referral_code():
	alpha = ['a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i', 'j', 'k', 'l', 'm', 'n', 'o', 'p', 'q', 'r', 's', 't', 'u', 'v', 'w', 'x', 'y', 'z']
	referral = ""

	for i in range(0,6):
		referral = referral + random.choice(alpha)

	return referral


def change_address(request):
	user = request.user
	profile = UserProfile.objects.get(user=user)


	return render_to_response(
		'change_address.html',
		{
		'profile':profile,
		},
		context)

@login_required
def process_phone_number(request):
	context = RequestContext(request)
	user = request.user

	if request.method == 'POST':
		phone = request.POST.get('phone')
		profile = UserProfile.objects.get(user=user)
		referral_code = Referral.objects.get(profile=profile).referral_code

		number_good = verify_phone(phone)

		if number_good[0]:
			account_sid = "ACa2d2fde5fb38917dc892c94654f345cd"
			auth_token = "d5b72594bce3487a3dff812a08bc8265"
			client = TwilioRestClient(account_sid, auth_token)
			
			msg = "Hey! Your friend " + user.first_name + " " + user.last_name + " is inviting you to Over Easy, the new breakfast delivery service! Simply go to overeasyapp.com and when you checkout, put in code " + referral_code + "."
			message = client.messages.create(to=number_good[1], 
				from_=settings.TWILIO_PHONE, 
				body=msg)

	return redirect('/profile')


def verify_phone(phone):
	if not re.match(r"^\(?([0-9]{3})\)?[-. ]?([0-9]{3})[-. ]?([0-9]{4})$", phone):
		error = "Please provide a valid phone number."
		return (False, error)
	return (True, phone)

