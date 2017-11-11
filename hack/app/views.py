from django.shortcuts import render
from django.views.decorators.csrf import csrf_exempt
from django.http import HttpResponse, HttpResponseRedirect
import re
from models import Farmer, BorrowTractor, LendTractor
from twilio.rest import TwilioRestClient 
# Create your views here.

import json
from math import radians, asin, sin, cos, sqrt
from operator import itemgetter

@csrf_exempt
def sms(request):
	print request.body
	sms_body = request.POST.get('Body')
	sms_id = request.POST.get('SmsMessageSid')
	sender,body = retrieve_messages(sms_id)
	list_of_numbers = re.findall('\\b\\d+\\b', body)

	if 'available' in body:
		lending = LendTractor.objects.create()
		lending.quantity = str(list_of_numbers[0])
		lending.date = str(list_of_numbers[1])
		lending.from_time = str(list_of_numbers[2])
		lending.to_time = str(list_of_numbers[3])
		lending.number = str(sender)
		lending.fullfilled = str(0)
		lending.save()

	elif 'needed' in body:
		borrow = BorrowTractor.objects.create()
		borrow.quantity = str(list_of_numbers[0])
		borrow.date = str(list_of_numbers[1])
		borrow.from_time = str(list_of_numbers[2])
		borrow.to_time = str(list_of_numbers[3])
		borrow.number = str(sender)
		borrow.fullfilled = str(0)
		farmer_number = str(sender)
		borrow.save()

		lending_tractors = LendTractor.objects.all()
		for tractor in lending_tractors:
			if tractor.quantity >= borrow.quantity and tractor.date == borrow.date and tractor.from_time <= borrow.from_time and tractor.to_time >= borrow.to_time:
				borrower_farmer = Farmer.objects.get(number=farmer_number)
				lender_farmer_number = tractor.number
				lender_farmer = Farmer.objects.get(number=lender_farmer_number)
				distance = get_distance(lender_farmer.lat, lender_farmer.lng, borrower_farmer.lat, borrower_farmer.lng)
				print str(distance) + "KM"
				print str(lender_farmer_number)

	else:
		print "Incorrect format"

def get_distance(lat1, lng1, lat2, lng2):
    radius_earth = 6371
    adwyze_lat = radians(float(lat1))
    adwyze_long = radians(float(lng1))
    friend_lat = radians(float(lat2))
    friend_long = radians(float(lng2))
    d_lat = friend_lat - adwyze_lat
    d_long = friend_long - adwyze_long
    under_root = sin(d_lat / 2)**2 + cos(adwyze_lat) * \
        cos(friend_lat) * ((sin(d_long) / 2)**2)
    d_sigma = 2 * asin(sqrt(under_root))
    distance = radius_earth * d_sigma
    return distance

def parse(string):
	pattern = ''

def retrieve_messages(message_id):
	ACCOUNT_SID = "ACfd8458e1b38af66c49017d5905dcfaf2" 
	AUTH_TOKEN = "dedea98e4e1ff2c7403667fdc8542373" 
 	client = TwilioRestClient(ACCOUNT_SID, AUTH_TOKEN) 
 	smss = client.sms.messages.list()
	sender = ''
	for sms in smss:
		if sms.sid == message_id:
			sender =  sms.from_
			body = sms.body
	return sender, body
def register_farmer(request):
	if(request.method == 'POST'):
		farmer = Farmer.objects.create()
		farmer.name = request.POST.get('name')
		farmer.number = request.POST.get('number')
		id = farmer.id
		farmer.save()
		return HttpResponseRedirect('getlocation/'+str(id))
	#message_id = "SM0cc0afc10d9814ff45fbafe176f66ed3"
	#retrieve_messages(message_id)
	return render(request, 'register_farmer.html')

def get_location(request, id):
	if(request.method == 'POST'):
		lat = request.POST.get('glat')
		lng = request.POST.get('glng')
		farmer = Farmer.objects.get(id=id)
		farmer.lat = lat
		farmer.lng = lng
		farmer.save()
		return HttpResponseRedirect('/admin')
	return render(request, 'get_location.html',{'id':id})

