from django.db import models
from orders.models import Order
from users.models import DriverProfile

class DriverOrder(models.Model):
	driver = models.ForeignKey(DriverProfile)
	order = models.ForeignKey(Order)

# Create your models here.
