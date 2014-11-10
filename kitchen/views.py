from django.template import RequestContext
from django.shortcuts import render_to_response, redirect
from django.conf import settings
from django.http import HttpResponse
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required

from datetime import datetime, date, time, timedelta

from users.models import UserProfile, DriverProfile, StaffProfile
from restaurants.models import Restaurant
from item.models import Item
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

		today = datetime.today().date() + timedelta(days=1)

		orders_to_display = []

		for entry in Entry.objects.filter(date=today).order_by('time'):
			for order in Order.objects.filter(entry=entry):
				orders_to_display.append(order)

		no_orders = False
		if len(orders_to_display) == 0:
			no_orders = True


		matrix = []
		items = Item.objects.all()
		entries = Entry.objects.filter(date=today).order_by('time')


		for entry in entries:
			entry_item = []
			for i in items:
				item = i
				count = 0
				for oi in OrderItem.objects.filter(item=item):
					if (oi.order.entry == entry):
						count = count + oi.quantity
				to_add = [entry, item, count]
				entry_item.append(to_add)
			matrix.append(entry_item)

		tomorrow = today + timedelta(days=1)

		orders_for_tomorrow = []

		for entry in Entry.objects.filter(date=tomorrow).order_by('time'):
			for order in Order.objects.filter(entry=entry):
				orders_for_tomorrow.append(order)

		no_orders_tomorrow = False

		if len(orders_for_tomorrow) == 0:
			no_orders_tomorrow = True

		return render_to_response(
			"kitchen.html",
			{
			'matrix':matrix,
			'no_orders':no_orders,
			'no_orders_tomorrow':no_orders_tomorrow,
			'orders_to_display':orders_to_display,
			'orders_for_tomorrow':orders_for_tomorrow,
			'items':items,
			'entries':entries,
			},
			context)

	return HttpResponse("You are not credentialed to view this area.")
