from django.template import RequestContext
from django.shortcuts import render_to_response, redirect
from django.conf import settings
from django.http import HttpResponse
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required

from datetime import datetime, date, time, timedelta

from users.models import UserProfile, DriverProfile, StaffProfile
from restaurants.models import Restaurant

from orders.models import Order, OrderItem
from drivers.models import DriverOrder
from cal.models import Entry

def view_driver(request):
	context = RequestContext(request)
	user = request.user

	able_to_access = False
	driver = ""

	for p in DriverProfile.objects.all():
		if p.user == user:
			able_to_access = True
			driver = p

	if able_to_access:

		today = datetime.today().date()

		orders_to_display = []
		for entry in Entry.objects.filter(date=today).order_by('time'):
			for do in DriverOrder.objects.filter(driver=driver):
				if do.order.entry == entry:
					orders_to_display.append(do.order)

		no_orders = False

		if len(orders_to_display) == 0:
			no_orders = True

		tomorrow = today + timedelta(days=1)

		orders_for_tomorrow = []
		for entry in Entry.objects.filter(date=tomorrow).order_by('time'):
			for do in DriverOrder.objects.filter(driver=driver):
				if do.order.entry == entry:
					orders_to_display.append(do.order)

		no_orders_tomorrow = False

		if len(orders_for_tomorrow) == 0:
			no_orders_tomorrow = True

		entries = Entry.objects.all()

		return render_to_response(
			"driver.html",
			{
			'today':today,
			'no_orders':no_orders,
			'no_orders_tomorrow':no_orders_tomorrow,
			'orders_to_display':orders_to_display,
			'orders_for_tomorrow':orders_for_tomorrow,
			},
			context)

	return HttpResponse("You are not credentialed to view this area.")
