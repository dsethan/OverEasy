from django.shortcuts import render, render_to_response, redirect
from django.shortcuts import render
from django.template import RequestContext
from django.http import HttpResponse, HttpResponseRedirect

from datetime import datetime, date, time, timedelta

from cal.models import Entry

def set_calendar(request):
	context = RequestContext(request)
	user = request.user

	if not user.is_superuser:
		return HttpResponse("You are not permissioned to be in this area.")

	else:
		today = datetime.today().date()
		week = today.isocalendar()[1]
		weekday = today.isocalendar()[2]
		mon = today - timedelta(days=weekday-1)

		if (weekday == 6) or (weekday == 7):
			week = week + 1
			mon = mon + timedelta(days=7)

		day_list = []

		m, t, w, th, f, s, su = [], [], [], [], [], [], []

		for i in range(0, 7):
			day = mon + timedelta(days=i)
			formatted_day = day.strftime("%A, %B %d")
			day_list.append(formatted_day)

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

		for j in [m, t, w, th, f, s, su]:
			sort_list_by_time(j)

		valid_to_add = True

		days = [m, t, w, th, f, s, su]

		for k in days:
			if len(k) > 0:
				valid_to_add = False
				break
				
		return render_to_response(
			'caladmin.html',
			{
			'day_list':day_list,
			'days':days
			},
			context)

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