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
import cart.views

@login_required
def display_menu(request, entry_id):
	context = RequestContext(request)
	user = request.user
	profile = users.views.return_associated_profile_type(user)

	entry = Entry.objects.get(id=entry_id)
	cart = cart.views.cart_exists(user, entry)

	if cart == False:
		new_cart = Cart(profile=profile, 
			entry=entry, 
			total=0)
		new_cart.save()
		cart = new_cart()

	if not cart_active(user, entry):
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
