from django.shortcuts import render
from cart.models import Cart
from users.models import UserProfile

import users.views

def cart_exists(user, entry):
	profile = users.views.return_associated_profile_type(user)

	for c in Cart.objects.all():
		if (c.profile == profile) and (c.entry == entry):
			return c

	return False

def cart_active(user, entry):
	profile = users.views.return_associated_profile_type(user)
	c = Cart.objects.filter(profile=profile, entry=entry)

	if c.open() and c.orders_still_open():
		return True

	return False
