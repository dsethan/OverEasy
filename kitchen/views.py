import re
from django.template import RequestContext
from django.shortcuts import render_to_response, redirect
from django.conf import settings
from django.http import HttpResponse
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required

from users.models import UserProfile, DriverProfile, StaffProfile
from restaurants.models import Restaurant
from demand.models import Demand

from pygeocoder import Geocoder
from googlemaps import GoogleMaps

def view_kitchen(request):


	return HttpResponse("KITCHEN")
