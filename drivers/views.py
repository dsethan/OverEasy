from django.template import RequestContext
from django.shortcuts import render_to_response, redirect
from django.conf import settings
from django.http import HttpResponse
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from django.contrib.auth.decorators import user_passes_test

from datetime import datetime, date, time, timedelta

from users.models import UserProfile, DriverProfile, StaffProfile
from restaurants.models import Restaurant

from orders.models import Order, OrderItem
from drivers.models import DriverOrder
from cal.models import Entry
from twilio.rest import TwilioRestClient

def send_text(profile, driver):
	account_sid = "ACa2d2fde5fb38917dc892c94654f345cd"
	auth_token = "d5b72594bce3487a3dff812a08bc8265"
	client = TwilioRestClient(account_sid, auth_token)
	msg = "Hey! " + str(profile.user.first_name) + "Your Over Easy driver " + str(driver.user.first_name ) + " is outside with your breakfast."	
	message = client.messages.create(to=profile.phone, 
		from_=settings.TWILIO_PHONE, 
		body=msg)

	return

def process_arrival(request):
	context = RequestContext(request)
	user = request.user
	if request.method == 'POST':
		order_id = request.POST.get('order_id')
		driver_id = request.POST.get('driver_id')

		order = Order.objects.get(id=order_id)
		driver = DriverProfile.objects.get(id=driver_id)

		profile = order.profile

		send_text(profile, driver)

		return HttpResponse("Finished text")



@user_passes_test(lambda u: u.is_superuser)
def manage_drivers(request):
	context = RequestContext(request)
	user = request.user

	if request.method == 'POST':
		driver_id = request.POST.get('driver_id')
		order_id = request.POST.get('order_id')

		driver = DriverProfile.objects.get(id=driver_id)
		order = Order.objects.get(id=order_id)

		driver_order = get_driver_order(order)

		if driver_order != None:
			driver_order_to_delete = DriverOrder.objects.get(order=order)
			driver_order_to_delete.delete()

			driver_order = DriverOrder(
				driver=driver,
				order=order)

			driver_order.save()

		else:
			driver_order = DriverOrder(
				driver=driver,
				order=order)

			driver_order.save()


	all_drivers = DriverProfile.objects.all()

	today = datetime.today().date() + timedelta(days=1)

	orders_to_display = []
	for entry in Entry.objects.filter(date=today).order_by('time'):
		for order in Order.objects.filter(entry=entry):
			print order
			orders_to_display.append(order)


	all_driver_orders = []

	for order in DriverOrder.objects.all():
		if order.order.entry.date == today:
			all_driver_orders.append(order)

	no_orders_today = False
	if len(orders_to_display) == 0:
		no_orders_today = True

	tomorrow = today + timedelta(days=1)

	orders_for_tomorrow = []

	for entry in Entry.objects.filter(date=tomorrow):
		for order in Order.objects.filter(entry=entry):
			orders_for_tomorrow.append(order)

	no_orders_tomorrow = False
	if len(orders_for_tomorrow) == 0:
		no_orders_tomorrow = True

	return render_to_response(
		"drivermgmt.html",
		{
		'user':user,
		'all_drivers':all_drivers,
		'orders_to_display':orders_to_display,
		'orders_for_tomorrow':orders_for_tomorrow,
		'no_orders_today':no_orders_today,
		'no_orders_tomorrow':no_orders_tomorrow,
		'today':today,
		'tomorrow':tomorrow,
		'all_driver_orders':all_driver_orders,
		},
		context)

def get_driver_order(order):
	exists = False
	driver_order = ""

	for do in DriverOrder.objects.all():
		if do.order == order:
			exists = True
			driver_order = do

	if not exists:
		return None

	return driver_order

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

		today = datetime.today().date() + timedelta(days=1)

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
			'driver':driver,
			},
			context)

	return HttpResponse("You are not credentialed to view this area.")
