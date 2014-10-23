import re
from django.template import RequestContext
from django.shortcuts import render_to_response, redirect
from django.conf import settings
from django.http import HttpResponse
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required

from users.models import UserProfile
from orders.models import Order, OrderItem

def display_profile(request):
	context = RequestContext(request)
	user = request.user
	profile = UserProfile.objects.get(user=user)
	orders = Order.objects.filter(profile=profile)

	no_orders_yet = False

	if len(orders) == 0:
		no_orders_yet = True

	return render_to_response(
		'profile.html',
		{
		'profile':profile,
		'orders':orders,
		'no_orders_yet':no_orders_yet,
		},
		context)

