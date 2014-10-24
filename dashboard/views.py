from django.shortcuts import render, render_to_response, redirect
from django.shortcuts import render
from django.template import RequestContext
from django.http import HttpResponse, HttpResponseRedirect
from django.conf import settings

from datetime import datetime, date, time, timedelta

from cal.models import Entry
from restaurants.models import Restaurant
from item.models import Item, ItemCategory

def set_menu(request):
	context = RequestContext(request)
	user = request.user

	if not user.is_superuser:
		return HttpResponse("You are not permissioned to be in this area.")

	else:
		categories = []
		items_by_cat = {}
		for cat in settings.ITEM_CATEGORIES:
			name = cat[0]
			items_by_cat[name] = ItemCategory.objects.filter(category=cat[1])
			categories.append(cat[1])
		
		return render_to_response(
			'menuadmin.html',
			{
			'items_by_cat':items_by_cat,
			'categories':categories,
			},
			context)

def initialize_new_menu_item(request):
	context = RequestContext(request)
	user = request.user

	item_name = request.POST.get('item_name')
	price = request.POST.get('price')
	cost = request.POST.get('cost')
	description = request.POST.get('description')
	prep_category = request.POST.get('prep_category')
	category = request.POST.get('category')

	new_item = Item(
		name=item_name,
		price=int(price),
		cost=int(cost),
		description=description,
		prep_category=prep_category
		)

	new_item.save()

	new_category = ItemCategory(
		item=new_item,
		category=category)

	new_category.save()

	return redirect('set_menu')



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

		if (weekday == 5) or (weekday == 6) or (weekday == 7):
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

		m = sort_list_by_time(m)
		t = sort_list_by_time(t)
		w = sort_list_by_time(w)
		th = sort_list_by_time(th)
		f = sort_list_by_time(f)
		s = sort_list_by_time(s)
		su = sort_list_by_time(su)

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
			'days':days,
			'valid_to_add':valid_to_add,
			},
			context)

def cal_process_add(request):
	context = RequestContext(request)

	available = request.POST.get("available")
	deliv_id = request.POST.get("deliv_id")

	entry_to_update = Entry.objects.get(id=deliv_id)
	entry_to_update.available = int(available)

	entry_to_update.save()

	return redirect('set_calendar')

def initialize_week(request):
	context = RequestContext(request)

	mon = request.POST.get("m")
	tue = request.POST.get("t")
	wed = request.POST.get("w")
	thu = request.POST.get("th")
	fri = request.POST.get("f")
	sat = request.POST.get("s")
	sun = request.POST.get("su")
	start_hour = int(request.POST.get("start_time_hour"))
	start_min = int(request.POST.get("start_time_min"))

	daily_entries = int(request.POST.get("num_entries"))
	window_length = int(request.POST.get("win_len"))

	days = [mon, tue, wed, thu, fri, sat, sun]

	today = datetime.today().date() + timedelta(days=7)
	
	week = today.isocalendar()[1]
	weekday = today.isocalendar()[2]

	weekday = today.isocalendar()[2]
	monday = today - timedelta(days=weekday-1)
	tuesday = today - timedelta(days=weekday-2)
	wednesday = today - timedelta(days=weekday-3)
	thursday = today - timedelta(days=weekday-4)
	friday = today - timedelta(days=weekday-5)
	saturday = today - timedelta(days=weekday-6)
	sunday = today - timedelta(days=weekday-7)

	if (weekday == 6) or (weekday == 7):
		week = week + 1
		monday = monday + timedelta(days=7)
		tuesday = tuesday + timedelta(days=7)
		wednesday = wednesday + timedelta(days=7)
		thursday = thursday + timedelta(days=7)
		friday = friday + timedelta(days=7)
		saturday = saturday + timedelta(days=7)
		sunday = sunday + timedelta(days=7)


	if mon == "on":
		start_time = time(start_hour, start_min)

		for k in range(daily_entries):
			new_entry = Entry(
				time = start_time,
				date = monday,
				restaurant = Restaurant.objects.get(id=1),
				length = window_length
				)

			new_entry.save()

			d = date(2000, 01, 01)
			dt = datetime.combine(d, start_time)
			start_dt = dt + timedelta(minutes=window_length)
			start_time = start_dt.time()

	if tue == "on":
		start_time = time(start_hour, start_min)

		for k in range(daily_entries):
			new_entry = Entry(
				time = start_time,
				date = tuesday,
				restaurant = Restaurant.objects.get(id=1),
				length = window_length
				)

			new_entry.save()

			d = date(2000, 01, 01)
			dt = datetime.combine(d, start_time)
			start_dt = dt + timedelta(minutes=window_length)
			start_time = start_dt.time()

	if wed == "on":
		start_time = time(start_hour, start_min)

		for k in range(daily_entries):
			new_entry = Entry(
				time = start_time,
				date = wednesday,
				restaurant = Restaurant.objects.get(id=1),
				length = window_length
				)

			new_entry.save()

			d = date(2000, 01, 01)
			dt = datetime.combine(d, start_time)
			start_dt = dt + timedelta(minutes=window_length)
			start_time = start_dt.time()

	if thu == "on":
		start_time = time(start_hour, start_min)

		for k in range(daily_entries):
			new_entry = Entry(
				time = start_time,
				date = thursday,
				restaurant = Restaurant.objects.get(id=1),
				length = window_length
				)

			new_entry.save()

			d = date(2000, 01, 01)
			dt = datetime.combine(d, start_time)
			start_dt = dt + timedelta(minutes=window_length)
			start_time = start_dt.time()

	if fri == "on":
		start_time = time(start_hour, start_min)

		for k in range(daily_entries):
			new_entry = Entry(
				time = start_time,
				date = friday,
				restaurant = Restaurant.objects.get(id=1),
				length = window_length
				)

			new_entry.save()

			d = date(2000, 01, 01)
			dt = datetime.combine(d, start_time)
			start_dt = dt + timedelta(minutes=window_length)
			start_time = start_dt.time()

	if sat == "on":
		start_time = time(start_hour, start_min)

		for k in range(daily_entries):
			new_entry = Entry(
				time = start_time,
				date = saturday,
				restaurant = Restaurant.objects.get(id=1),
				length = window_length
				)

			new_entry.save()

			d = date(2000, 01, 01)
			dt = datetime.combine(d, start_time)
			start_dt = dt + timedelta(minutes=window_length)
			start_time = start_dt.time()

	if sun == "on":
		start_time = time(start_hour, start_min)

		for k in range(daily_entries):
			new_entry = Entry(
				time = start_time,
				date = sunday,
				restaurant = Restaurant.objects.get(id=1),
				length = window_length
				)

			new_entry.save()

			d = date(2000, 01, 01)
			dt = datetime.combine(d, start_time)
			start_dt = dt + timedelta(minutes=window_length)
			start_time = start_dt.time()

	return redirect('set_calendar')

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