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

	items_with_quantity = user_cart.get_items_and_quantities()

	item_urls = {}
	for item in user_cart.get_cart_items():
		item_urls[item.id] = get_url_for_item(item.item)

	item_names = []

	for cat in settings.ITEM_CATEGORIES:
		name = cat[0].upper()
		items_by_cat[name] = ItemCategory.objects.filter(category=cat[1])

	cart_more_than_one = False

	if len(items_with_quantity.keys()) > 0:
		cart_more_than_one = True

	cart_id = user_cart.id

	total = user_cart.view_order_total_in_usd()

	total_price = user_cart.get_total_price_of_cart()

	all_items = Item.objects.all()

	return render_to_response(
		'menu.html',
		{
		'all_items':all_items,
		'entry':entry,
		'entry_id':entry_id,
		'user':user,
		'profile':profile,
		'items_by_cat':items_by_cat,
		'cart_items':cart_items,
		'items_with_quantity':items_with_quantity,
		'cart_id':cart_id,
		'cart_more_than_one':cart_more_than_one,
		'item_urls':item_urls,
		'total':total,
		'total_price':total_price,
		},
		context)


def remove_from_cart(request):
	context = RequestContext(request)
	user = request.user

	if request.method == 'POST':
		cart_item_id = request.POST.get('cart_item_id')
		cart_item = CartItem.objects.get(id=int(cart_item_id))
		entry_id = request.POST.get('entry_id')
		cart_item.delete()

		string_to_redirect = "/cal/" + str(entry_id) + "/"
		#return HttpResponse(entry_id)

		return redirect(string_to_redirect)

	return redirect('/cal/')


def get_url_for_item(item):
	base_str_url = "/static/img/cart/"
	end_str_url = ".png"
	url = base_str_url + str(item.id) + end_str_url
	return url


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

	return redirect('/menu')


@login_required
def user_cart_no_longer_active(request):
	context = RequestContext(request)
	message = "Sorry, but the window you chose is no longer active. Want to try another?"
	return render_to_response(
		'order_unavailable.html',
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
