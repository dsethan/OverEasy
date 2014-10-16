from django.contrib import admin
from payments.models import Card

class CardAdmin(admin.ModelAdmin):
	list_display = ('user', 'customer', 'token')

admin.site.register(Card, CardAdmin)