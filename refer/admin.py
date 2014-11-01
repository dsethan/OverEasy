from django.contrib import admin
from refer.models import Referral, ReferralMatches


class ReferralAdmin(admin.ModelAdmin):
	list_display = ('profile', 'referral_code', 'credits')

class ReferralMatchesAdmin(admin.ModelAdmin):
	list_display = ('referrer', 'referred')

admin.site.register(Referral, ReferralAdmin)
admin.site.register(ReferralMatches, ReferralMatchesAdmin)