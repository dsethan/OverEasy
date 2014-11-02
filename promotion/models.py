from django.db import models
from users.models import UserProfile


class Referral(models.Model):
	profile = models.ForeignKey(UserProfile)
	referral_code = models.CharField(max_length=20)
	credits = models.IntegerField(default=0)

	def get_credits_in_usd(self):
		total = self.credits
		total = int(total)
		self_str = str(total)
		cents = self_str[-2:]
		dollars = self_str[:-2]
		if len(dollars) == 0:
			dollars = "0"
		if len(cents) == 1:
			cents = "0" + cents
		return "$" + dollars + "." + cents

	def get_num_referrals(self):
		return ReferralMatches.objects.filter(referrer=profile)

	def __unicode__(self):
		return self.profile.user.first_name + " " + self.profile.user.last_name + " " + self.referral_code

class ReferralMatches(models.Model):
	referrer = models.ForeignKey(UserProfile, related_name="referrer")
	referred = models.ForeignKey(UserProfile)