from django.shortcuts import render
from django.http import HttpResponse, HttpResponseRedirect
from django.template import RequestContext
from django.shortcuts import render_to_response, HttpResponseRedirect
from django.contrib.auth.decorators import login_required
from django.conf import settings

from cal.models import Entry
from users.models import UserProfile
from cart.models import Cart, CartItem
from payments.models import Card
from orders.models import Order, OrderItem

import users.views

import stripe

@login_required
def checkout(request):
	context = RequestContext(request)
	user = request.user
	profile = UserProfile.objects.get(user=user)

	if request.method == 'POST':
		entry_id = request.POST.get('entry_id')
		cart_id = request.POST.get('cart_id')

		entry = Entry.objects.get(id=int(entry_id))
		cart = Cart.objects.get(id=int(cart_id))
		cart_items = cart.get_items()
		items_with_quantity = cart.get_item_names_and_quantities()

		cards = Card.objects.filter(user=user)

		card_on_file = False
		if len(cards) > 0:
			card_on_file = True

		total_price = cart.get_total_price_of_cart()
		cart_id = cart.id

		return render_to_response(
			'checkout.html',
			{
			'profile':profile,
			'user':user,
			'cart':cart,
			'cart_id':cart_id,
			'items_with_quantity':items_with_quantity,
			'entry':entry,
			'cards':cards,
			'total_price':total_price,
			'card_on_file':card_on_file,
			},
			context)


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

	if request.method == 'POST':
		cart_id = request.POST.get('cart_id')
		total_price = request.POST.get('total_price')
		token = request.POST['stripeToken']
		stripe.api_key = settings.STRIPE
		last_four = request.POST['last4']
		brand = request.POST['brand']

		customer = stripe.Customer.create(
			card=token,
			description=user.username)

		new_card = Card(
			user = user,
			customer=customer.id,
			token=token,
			)

		new_card.save()

		company = ""
		if brand == "Visa":
			company = 'VIS'
		elif brand == "MasterCard":
			company = 'MCD'
		elif brand == "American Express":
			company = 'AME'
		elif brand == "Discover":
			company = 'DIS'
		else:
			brand = 'VIS'

		new_card_data = CardData(
			card = new_card,
			company = company,
			last_four = last_four
			)

		new_card_data.save()

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