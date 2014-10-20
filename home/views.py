from django.template import RequestContext
from django.shortcuts import render_to_response, redirect

from users.models import UserProfile, DriverProfile, StaffProfile
from restaurants.models import Restaurant
from demand.models import Demand

from pygeocoder import Geocoder
from googlemaps import GoogleMaps
