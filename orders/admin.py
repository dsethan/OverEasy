from django.contrib import admin
from orders.models import Order, OrderItem

class OrderAdmin(admin.ModelAdmin):
	list_display = ('profile', 'total', 'entry', 'date_placed', 'time_placed', 'date_delivered', 'time_delivered', 'status', 'order_rating')

class OrderItemAdmin(admin.ModelAdmin):
	list_display = ('item', 'order', 'quantity')

admin.site.register(Order, OrderAdmin)
admin.site.register(OrderItem, OrderItemAdmin)