from django.contrib import admin
from users.models import UserProfile, DriverProfile, StaffProfile

class UserProfileAdmin(admin.ModelAdmin):
	list_display = ('user', 'address', 'city', 'state', 'phone')

class DriverProfileAdmin(admin.ModelAdmin):
	list_display = ('user', 'address', 'city', 'state', 'phone')

class StaffProfileAdmin(admin.ModelAdmin):
	list_display = ('user', 'address', 'city', 'state', 'phone')

admin.site.register(UserProfile, UserProfileAdmin)

admin.site.register(DriverProfile, DriverProfileAdmin)

admin.site.register(StaffProfile, StaffProfileAdmin)