from django.contrib import admin
from cal.models import Entry

class EntryAdmin(admin.ModelAdmin):
	list_display = ('date', 'time', 'available', 'demand', 'restaurant', 'length', 'shutoff_hour', 'shutoff_min')

admin.site.register(Entry, EntryAdmin)
