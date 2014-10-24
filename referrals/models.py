import random

from django.db import models
from users.models import UserProfile
from django.contrib.auth.models import User
from django.conf import settings

from twilio.rest import TwilioRestClient

class TextReferral(models.Model):
	initiator = models.ForeignKey(User)
	target_phone = models.CharField(max_length=15)
	initator_code = models.CharField(max_length=15)
	active = models.BooleanField(default=False)

	def is_target_in_system(self):
		for user in User.objects.all():
			if user.username == target_email:
				return False
		return True

	def verify_phone(phone, self):
		if not re.match(r"^\(?([0-9]{3})\)?[-. ]?([0-9]{3})[-. ]?([0-9]{4})$", self.phone):
			error = "Please provide a valid phone number."
			return (False, error)
		return (True, phone)

	def verify_not_signed_up(self):
		for profile in UserProfile.objects.all():
			if profile.phone_just_digits() == self.target_phone:
				return False

		return True

	def send_text_to_target(self):
		account_sid = "ACa2d2fde5fb38917dc892c94654f345cd"
		auth_token = "d5b72594bce3487a3dff812a08bc8265"
		client = TwilioRestClient(account_sid, auth_token)
		 
		msg = "Hello there!" + str(self.initiator.first_name) + " " + str(self.initiator.last_name) + " has invited you to sign up for Over Easy! Go to overeasyapp.com to sign up. Put in code " + self.initiator_code + " for a free breakfast!"
		message = client.messages.create(to=self.target_phone, 
			from_=settings.TWILIO_PHONE, 
			body=msg)

