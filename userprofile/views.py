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
from refer.models import Referral

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


