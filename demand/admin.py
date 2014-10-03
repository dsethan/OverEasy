from django.contrib import admin
from demand.models import Demand

class DemandAdmin(admin.ModelAdmin):
	list_display = ('first', 'last', 'email', 'phone', 'address')

admin.site.register(Demand, DemandAdmin)
