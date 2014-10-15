from django.shortcuts import render
from django.http import HttpResponse, HttpResponseRedirect
from django.template import RequestContext
from django.shortcuts import render_to_response
from django.contrib.auth.decorators import login_required

from cal.models import Entry
from item.models import Item
from django.contrib.auth.models import User
from users.models import UserProfile
from cart.models import Cart, CartItem

import users.views

@login_required
def display_menu(request, entry_id=False):
	context = RequestContext(request)
	user = request.user

	if entry_id == False:
		return HttpResponse("You must first select a delivery window.")


	profile = users.views.return_associated_profile_type(user)
	print entry_id
	entry = Entry.objects.get(id=entry_id)
	user_cart = cart_exists(user, entry)

	if user_cart == False:
		new_cart = Cart(profile=profile, 
			entry=entry, 
			total=0)
		new_cart.save()
		user_cart = new_cart

	if not user_cart.is_active():
		message = "Sorry, but the window you chose is no longer active. Want to try another?"
		return render_to_response(
			'order_unavailable',
			{
			'message':message,
			},
			context)

	items = Item.objects.all()

	return render_to_response(
		'menu.html',
		{
		'entry':entry,
		'entry_id':entry_id,
		'user':user,
		'profile':profile,
		'items':items,
		},
		context)


def cart_exists(user, entry):
	profile = users.views.return_associated_profile_type(user)

	for c in Cart.objects.all():
		if (c.profile == profile) and (c.entry == entry):
			return c

	return False
