from django.shortcuts import render
from django.views.decorators.csrf import csrf_exempt
import re
# Create your views here.
@csrf_exempt
def sms(request):
	print request.body
	print request.POST.get('Body')

def parse(string):
	pattern = ''

