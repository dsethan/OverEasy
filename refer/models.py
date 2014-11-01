from django.db import models
from users.models import UserProfile


class Referral(models.Model):
	profile = models.ForeignKey(UserProfile)
	referral_code = models.CharField(max_length=20)
	credits = models.IntegerField(default=0)

	def get_num_referrals(self):
		return ReferralMatches.objects.filter(referrer=profile)

	def __unicode__(self):
		return self.profile.user.first_name + " " + self.profile.user.last_name + " " + self.referral_code

class ReferralMatches(models.Model):
	referrer = models.ForeignKey(UserProfile, related_name="referrer")
	referred = models.ForeignKey(UserProfile)