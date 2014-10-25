from django.template import RequestContext
from django.shortcuts import render_to_response, redirect
from django.conf import settings
from django.http import HttpResponse
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required

from users.models import UserProfile, DriverProfile, StaffProfile
from restaurants.models import Restaurant

from orders.models import Order, OrderItem

def view_kitchen(request):
	context = RequestContext(request)
	user = request.user

	able_to_access = False
	for p in StaffProfile.objects.all():
		if p.user == user:
			able_to_access = True

	if able_to_access:

		today = datetime.today().date()

		orders_to_display = []
		for order in Order.objects.all():
			if order.entry.date == today:
				orders_to_display.append(order)

		return render_to_response(
			"kitchen.html",
			{
			'orders_to_display':orders_to_display,
			},
			context)

	return HttpResponse("You are not credentialed to view this area.")
