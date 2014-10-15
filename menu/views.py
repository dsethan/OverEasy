from django.shortcuts import render
from django.http import HttpResponse, HttpResponseRedirect
from django.template import RequestContext
from django.shortcuts import render_to_response, redirect
from django.contrib.auth.decorators import login_required
from django.conf import settings

from cal.models import Entry
from item.models import Item, ItemCategory
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
	entry = Entry.objects.get(id=entry_id)
	user_cart = cart_exists(user, entry)

	if user_cart == False:
		new_cart = Cart(profile=profile, 
			entry=entry, 
			total=0)
		new_cart.save()
		user_cart = new_cart

	if not user_cart.is_active():
		return user_cart_no_longer_active(request)

	items_by_cat = {}

	cart_items = CartItem.objects.filter(cart=user_cart)

	items_with_quantity = {}

	item_names = []

	for k in cart_items:
		item_names.append(k.item.name)

	for i in item_names:
		if i not in items_with_quantity.keys():
			items_with_quantity[i] = item_names.count(i)
		print items_with_quantity

	for cat in settings.ITEM_CATEGORIES:
		name = cat[0]
		items_by_cat[name] = ItemCategory.objects.filter(category=cat[1])

	return render_to_response(
		'menu.html',
		{
		'entry':entry,
		'entry_id':entry_id,
		'user':user,
		'profile':profile,
		'items_by_cat':items_by_cat,
		'cart_items':cart_items,
		'items_with_quantity':items_with_quantity,
		},
		context)

@login_required
def add_item_to_cart(request):
	context = RequestContext(request)
	user = request.user

	if request.method == 'POST':
		item_id = request.POST.get('item_id')
		entry_id = request.POST.get('entry_id')
		item = Item.objects.get(id=int(item_id))
		entry = Entry.objects.get(id=int(entry_id))

		user_cart = cart_exists(user, entry)

		if not user_cart.is_active():
			return user_cart_no_longer_active(request)

		if user_cart == False:
			return redirect('/cal')

		else:
			cart_item_to_add = CartItem(
				cart=user_cart,
				item=item,
				qty=1)
			cart_item_to_add.save()

			return display_menu(request, entry_id)


@login_required
def user_cart_no_longer_active(request):
	context = RequestContext(request)
	message = "Sorry, but the window you chose is no longer active. Want to try another?"
	return render_to_response(
		'order_unavailable',
		{
		'message':message
		},
		context)

def cart_exists(user, entry):
	profile = users.views.return_associated_profile_type(user)

	for c in Cart.objects.all():
		if (c.profile == profile) and (c.entry == entry):
			return c

	return False
