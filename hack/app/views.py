from django.shortcuts import render
from django.views.decorators.csrf import csrf_exempt
from django.http import HttpResponse, HttpResponseRedirect
import re
from models import Farmer, BorrowTractor, LendTractor
from twilio.rest import TwilioRestClient 
import urllib2
# Create your views here.

import json
from math import radians, asin, sin, cos, sqrt, ceil
from operator import itemgetter

def send_sms(message,number):
	number = number[3:]
	print number
	urltosend = 'https://control.msg91.com/api/sendhttp.php?authkey=132727AshR9z6QU9Dg58416307&mobiles='+number+'&message='+message+'&sender=ELTSPY&route=4'
	response = urllib2.urlopen(urltosend).read()
	print response

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
		farmer_number = str(sender)
		lending.fullfilled = str(0)
		lending.save()
		needed_tractors = BorrowTractor.objects.all()
		for tractor in needed_tractors:
			if tractor.quantity <= lending.quantity and tractor.date == lending.date and tractor.from_time >= lending.from_time and tractor.to_time <= lending.to_time and tractor.fullfilled=="0":
				lender_farmer = Farmer.objects.get(number=farmer_number)
				borrower_farmer_number = tractor.number
				borrower_farmer = Farmer.objects.get(number=borrower_farmer_number)
				distance = get_distance(lender_farmer.lat, lender_farmer.lng, borrower_farmer.lat, borrower_farmer.lng)
				distance = (ceil(distance*100)/100) 
				borrower_text = "YOU HAVE BEEN PAIRED WITH A FARMER FOR A TRACTOR. THE FARMER IS  " + str(distance) + " KM away. Number is =  " + str(lender_farmer.number) 
 				lender_text = "YOU HAVE BEEN PAIRED WITH A FARMER FOR A TRACTOR. THE FARMER IS  " + str(distance) + " KM away. Number is =  " + str(borrower_farmer.number)
 				send_sms(borrower_text,borrower_farmer.number)
 				send_sms(lender_text,lender_farmer.number)
 				break

	elif 'needed' in body:
		print ' IN NEEDED CONDITION '
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
			print 'IN LOOP OF LENDING'
			if tractor.quantity >= borrow.quantity and tractor.date == borrow.date and tractor.from_time <= borrow.from_time and tractor.to_time >= borrow.to_time and tractor.fullfilled=="0":
				print 'LOGIC PASSED'
				borrower_farmer = Farmer.objects.get(number=farmer_number)
				lender_farmer_number = tractor.number
				lender_farmer = Farmer.objects.get(number=lender_farmer_number)
				distance = get_distance(lender_farmer.lat, lender_farmer.lng, borrower_farmer.lat, borrower_farmer.lng)
				distance = (ceil(distance*100)/100) 
				print distance
				borrower_text = 'THE FARMER IS  ' + str(distance) + ' KM away. Number is =  ' + str(lender_farmer.number) 
 				lender_text = 'THE FARMER IS  ' + str(distance) + ' KM away. Number is =  '+ str(borrower_farmer.number)
 				send_sms(borrower_text,borrower_farmer.number)
 				send_sms(lender_text,lender_farmer.number)
 				print 'OK'
 				break

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

def stress_location(lat, lng):
	pass


