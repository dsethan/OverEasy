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
from cal.models import Entry

def view_kitchen(request):
	context = RequestContext(request)
	user = request.user

	able_to_access = False
	for p in StaffProfile.objects.all():
		if p.user == user:
			able_to_access = True

	if able_to_access:

		today = datetime.today().date()

		today_entries = Entry.objects.filter(date=tomorrow)

		orders_for_today = []

		for entry in today_entries:
			orders = entry.get_all_orders_for_entry():
			for order in orders:
				orders_for_today.append(order)

		no_orders_today = False

		if len(no_orders_today) == 0:
			no_orders_today = True

		tomorrow = today + timedelta(days=1)

		tomorrow_entries = Entry.objects.filter(date=tomorrow)

		orders_for_tomorrow = []

		for entry in tomorrow_entries:
			orders = entry.get_all_orders_for_entry():
			for order in orders:
				orders_for_tomorrow.append(order)

		no_orders_tomorrow = False

		if len(orders_for_tomorrow) == 0:
			no_orders_tomorrow = True

		return render_to_response(
			"kitchen.html",
			{
			'no_orders':no_orders,
			'no_orders_tomorrow':no_orders_tomorrow,
			'orders_to_display':orders_to_display,
			'orders_for_tomorrow':orders_for_tomorrow,
			},
			context)

	return HttpResponse("You are not credentialed to view this area.")
