import random
import twilio

from django.db import models
from django.contrib.auth.models import User

class Referral(models.Model):
	initiator = models.ForeignKey(User)
	target_phone = models.CharField(max_length=15)
	initator_code = models.CharField(max_length=15)
	active = models.BooleanField(default=True)
	percent_discount = models.IntegerField(default=0)
	dollar_discount = models.IntegerField(default=0)

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

	def generate_invite_code(self):
		alpha = ['A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I', 'J', 'K', 'L', 'M', 'N', 'O', 'P', 'Q', 'R', 'S', 'T', 'U', 'V', 'W', 'X', 'Y', 'Z']
		a1 = random.choice(alpha)
		a2 = random.choice(alpha)
		a3 = random.choice(alpha)
		a4 = random.choice(alpha)
		a5 = random.choice(alpha)
		a6 = random.choice(alpha)

		invite_string = a1+a2+a3+a4+a5+a6

		for r in Referral.objects.all():
			if r.initiator_code == invite_string:
				return generate_invite_code(self)

		return invite_string


