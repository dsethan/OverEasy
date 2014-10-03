from django.contrib import admin
from restaurants.models import Restaurant

class RestaurantAdmin(admin.ModelAdmin):
	list_display = ('name', 'address1', 'address2', 'city', 'state', 'max_radius')

admin.site.register(Restaurant, RestaurantAdmin)
