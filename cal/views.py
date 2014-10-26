from django.shortcuts import render, render_to_response, redirect
from django.template import RequestContext
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse, HttpResponseRedirect

from datetime import datetime, date, time, timedelta

from cal.models import Entry
import users.views
import menu.views

@login_required
def render_first_look_calendar(request):

	context = RequestContext(request)
	user = request.user
	profile = users.views.return_associated_profile_type(user)

	if profile == None:
		return HttpResponse("Unfortunately, we are not currently" +
			" serving in your area.")

	today = datetime.today().date()
	week = today.isocalendar()[1]
	weekday = today.isocalendar()[2]
	mon = today - timedelta(days=weekday-1)

	if (weekday == 5) or (weekday == 6) or (weekday == 7):
		week = week + 1
		mon = mon + timedelta(days=7)

	m, t, w, th, f, s, su = [], [], [], [], [], [], []

	day_list = []

	for i in range(0, 5):
		day = mon + timedelta(days=i)
		formatted_weekday = day.strftime("%a")
		formatted_day = day.strftime("%B %d")
		day_list.append((formatted_weekday, formatted_day))

		if i == 0:
			m = Entry.objects.filter(date=day)
		if i == 1:
			t = Entry.objects.filter(date=day)
		if i == 2:
			w = Entry.objects.filter(date=day)
		if i == 3:
			th = Entry.objects.filter(date=day)
		if i == 4:
			f = Entry.objects.filter(date=day)
		if i == 5:
			s = Entry.objects.filter(date=day)
		if i == 6:
			su = Entry.objects.filter(date=day)

	m = sort_list_by_time(m)
	t = sort_list_by_time(t)
	w = sort_list_by_time(w)
	th = sort_list_by_time(th)
	f = sort_list_by_time(f)
	s = sort_list_by_time(s)
	su = sort_list_by_time(su)

	# TO ADD BACK
	days = [m, t, w, th, f, s, su]

	return render_to_response(
		'initial_calendar.html',
		{
		'days':days,
		'day_list':day_list,
		'today':today,
		'user':user,
		},
		context)

@login_required
def render_second_look_calendar(request):

	context = RequestContext(request)
	user = request.user
	profile = users.views.return_associated_profile_type(user)

	if profile == None:
		return HttpResponse("Unfortunately, we are not currently" +
			" serving in your area.")

	today = datetime.today().date()
	week = today.isocalendar()[1]
	weekday = today.isocalendar()[2]
	mon = today - timedelta(days=weekday-1)

	if (weekday == 5) (weekday == 6) or (weekday == 7):
		week = week + 1
		mon = mon + timedelta(days=7)

	m, t, w, th, f, s, su = [], [], [], [], [], [], []

	day_list = []

	for i in range(0, 5):
		day = mon + timedelta(days=i)
		formatted_weekday = day.strftime("%a")
		formatted_day = day.strftime("%B %d")
		day_list.append((formatted_weekday, formatted_day))

		if i == 0:
			m = Entry.objects.filter(date=day)
		if i == 1:
			t = Entry.objects.filter(date=day)
		if i == 2:
			w = Entry.objects.filter(date=day)
		if i == 3:
			th = Entry.objects.filter(date=day)
		if i == 4:
			f = Entry.objects.filter(date=day)
		if i == 5:
			s = Entry.objects.filter(date=day)
		if i == 6:
			su = Entry.objects.filter(date=day)

	m = sort_list_by_time(m)
	t = sort_list_by_time(t)
	w = sort_list_by_time(w)
	th = sort_list_by_time(th)
	f = sort_list_by_time(f)
	s = sort_list_by_time(s)
	su = sort_list_by_time(su)

	days = [m, t, w, th, f]
	
	message = "Aw, man! That time is no longer available."

	return render_to_response(
		'calendar.html',
		{
		'message':message,
		'days':days,
		'day_list':day_list,
		'today':today,
		'user':user,
		},
		context)

def process_cal(request, entry_id):
	context = RequestContext(request)
	entry = Entry.objects.get(id=entry_id)
	if entry.orders_still_open():
		entry.demand = entry.demand + 1
		entry.save()
		return menu.views.display_menu(request, entry_id)
	else:
		entry.demand = entry.demand + 1
		entry.save()
		return redirect('render_second_look_calendar')

def sort_list_by_time(times):
	sorted_times = []

	for t in times:
		formatted = t.time.strftime("%I:%M")
		sorted_times.append(formatted)

	sorted_times = sorted(sorted_times)

	original_entries = []
	for k in sorted_times:
		for t in times:
			if k == t.time.strftime("%I:%M"):
				original_entries.append(t)

	return original_entries