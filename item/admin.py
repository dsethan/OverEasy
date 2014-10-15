from django.contrib import admin
from item.models import Item, ItemCategory

class ItemAdmin(admin.ModelAdmin):
	list_display = ('name', 'price', 'cost', 'description', 'prep_category', 'number_ordered', 'total_spent', 'available')

class ItemCategoryAdmin(admin.ModelAdmin):
	list_display = ('item', 'category')

admin.site.register(Item, ItemAdmin)
admin.site.register(ItemCategory, ItemCategoryAdmin)