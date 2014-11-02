import random

from django.shortcuts import render, render_to_response, redirect
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
from promotion.models import Referral, ReferralMatches

import users.views
import checkout.views

import stripe
from twilio.rest import TwilioRestClient

@login_required
def process_referral(request):
	context = RequestContext(request)
	user = request.user

	if request.method == 'POST':
		user_profile = UserProfile.objects.get(user=user)
		code = request.POST.get('code')
		referral_user_profile = find_user_for_code(code)

		if referral_user_profile == False:
			message = "Sorry, that code is not in our system."
			return render_to_response(
				"refer_response.html",
				{
				'message':message,
				},
				context) 

		orders = Order.objects.filter(profile=user_profile)

		match_already_in = False

		for rm in ReferralMatches.objects.all():
			if (rm.referrer == referral_user_profile) and (rm.referred == user_profile):
				match_already_in = True

		if len(orders) > 1:
			message = "Sorry, referral codes can only be applied upon your first order."
			return render_to_response(
				"refer_response.html",
				{
				'message':message,
				},
				context) 

		if referral_user_profile == user_profile:
			message = "Sorry, you cannot use your own referral code."

			return render_to_response(
				"refer_response.html",
				{
				'message':message,
				},
				context) 

		if match_already_in:
			message = "Sorry, you cannot use a referral code more than once."
			return render_to_response(
				"refer_response.html",
				{
				'message':message,
				},
				context) 

		else:
			referral = Referral.objects.get(referral_code=code)

			referral_match = ReferralMatches(
				referrer=referral.profile,
				referred=user_profile)

			referral_match.save()
			referral.credits = referral.credits + 1000 # inc by 10 dollars
			referral.save()
			message = "You just gave your friend a free $10 credit! Go to your profile to send your referral code to receive your own credits."

			return render_to_response(
				"refer_response.html",
				{
				'message':message,
				},
				context) 





def find_user_for_code(code):
	for r in Referral.objects.all():
		if r.referral_code == code:
			return r.profile

	return False
from django.shortcuts import render

# Create your views here.
