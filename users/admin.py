from django.contrib import admin
from users.models import UserProfile

class UserProfileAdmin(admin.ModelAdmin):
	list_display = ('user', 'address', 'city', 'state', 'phone')

class DriverProfileAdmin(admin.ModelAdmin):
	list_display = ('user', 'address', 'city', 'state', 'phone')

class StaffProfileAdmin(admin.ModelAdmin):
	list_display = ('user', 'address', 'city', 'state', 'phone')

admin.site.register(UserProfile, UserProfileAdmin)
