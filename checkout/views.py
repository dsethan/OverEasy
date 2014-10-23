from django.shortcuts import render
from django.http import HttpResponse, HttpResponseRedirect
from django.template import RequestContext
from django.shortcuts import render_to_response, HttpResponseRedirect
from django.contrib.auth.decorators import login_required
from django.conf import settings

from cal.models import Entry
from users.models import UserProfile
from cart.models import Cart, CartItem
from payments.models import Card, CardAttributes
from orders.models import Order, OrderItem

import users.views

import stripe

@login_required
def checkout(request):
	context = RequestContext(request)
	user = request.user
	profile = UserProfile.objects.get(user=user)

	if request.method == 'POST':
		stripe.api_key = settings.STRIPE
		entry_id = request.POST.get('entry_id')
		cart_id = request.POST.get('cart_id')
		entry = Entry.objects.get(id=int(entry_id))
		cart = Cart.objects.get(id=int(cart_id))
		cart_items = cart.get_items()
		items_with_quantity = cart.get_items_and_quantities()

		#urls = get_url_for_item(cart_items)

		cards = Card.objects.filter(user=user)

		attributes = []
		for card in cards:
			attributes_for_card = CardAttributes.objects.get(card=card)
			attributes.append(attributes_for_card)

		card_on_file = False
		if len(cards) > 0:
			card_on_file = True

		total_price = cart.get_total_price_of_cart()
		cart_id = cart.id

		return render_to_response(
			'checkout.html',
			{
			#'urls':urls,
			'entry':entry,
			'profile':profile,
			'user':user,
			'cart':cart,
			'cart_id':cart_id,
			'items_with_quantity':items_with_quantity,
			'entry':entry,
			'cards':cards,
			'total_price':total_price,
			'card_on_file':card_on_file,
			'attributes':attributes,
			},
			context)

	return HttpResponse("You must first select some items from the cart!")

@login_required
def process_existing_card(request):
	context = RequestContext(request)
	user = request.user

	if request.method == 'POST':
		cart_id = request.POST.get('cart_id')
		token = request.POST.get('card_token')
		cart = Cart.objects.get(id=cart_id)
		total_price = cart.get_total_price_of_cart()

		card = Card.objects.get(token=token)

		stripe.api_key = settings.STRIPE

		stripe.Charge.create(
			amount = int(total_price),
			currency = "usd",
			customer = card.customer
			)

		return create_order(cart_id, user, context)

	return HttpResponse("Uh oh! Something went wrong :(")

@login_required
def process_new_card(request):
	context = RequestContext(request)
	user = request.user
	stripe.api_key = settings.STRIPE


	if request.method == 'POST':
		cart_id = request.POST.get('cart_id')
		total_price = request.POST.get('total_price')
		token = request.POST['stripeToken']
		#last_four = request.POST.get('last4')
		#brand = request.POST.get('brand')

		customer = stripe.Customer.create(
			card=token,
			description=user.username)

		data = customer.cards.data[0]
		exp_month = data["exp_month"]
		exp_year = data["exp_year"]
		brand = data["brand"]
		last_four = data["last4"]

		new_card = Card(
			user = user,
			customer=customer.id,
			token=token,
			)

		new_card.save()

		new_card_attributes = CardAttributes(
			card = new_card,
			brand = brand,
			exp_month = exp_month,
			exp_year = exp_year,
			last_four = last_four
			)

		new_card_attributes.save()

		stripe.Charge.create(
			amount = int(total_price),
			currency="usd",
			customer=new_card.customer,
			)

		cart_id = int(cart_id)

		return create_order(cart_id, user, context)

def create_order(cart_id, user, context):
	cart = Cart.objects.get(id=cart_id)
	items = cart.get_items_and_quantities()
	profile = users.views.return_associated_profile_type(user)
	entry = cart.entry

	

	new_order = Order(
		profile=profile,
		total=cart.get_total_price_of_cart(),
		entry=entry,
		status='PDG',
		)

	new_order.save()

	for item in items.keys():
		new_order_item = OrderItem(
			item=item,
			order=new_order,
			quantity=items[item]
			)
		new_order_item.save()

	entry.available = entry.available - 1
	entry.save()

	cart.cart_still_active = False
	cart.delete()

	return render_to_response(
		'successful_charge.html',
		{
		},
		context)

def get_url_for_item(item):
	base_str_url = "/static/img/cart/"
	end_str_url = ".png"
	url = base_str_url + str(item.id) + end_str_url
	return url