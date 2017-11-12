from __future__ import unicode_literals

from django.db import models

class Farmer(models.Model):
	name = models.CharField(max_length=100, blank=True, null=True)
	number = models.CharField(max_length=100, blank=True, null=True)
	lat = models.CharField(max_length=100, blank=True, null=True)
	lng = models.CharField(max_length=100, blank=True, null=True)

class LendTractor(models.Model):
	number = models.CharField(max_length=100, blank=True, null=True)
	date = models.CharField(max_length=100, blank=True, null=True)
	from_time = models.CharField(max_length=100, blank=True, null=True)
	to_time = models.CharField(max_length=100, blank=True, null=True)
	quantity = models.CharField(max_length=100, blank=True, null=True)
	fullfilled = models.CharField(max_length=100, blank=True, null=True)

class BorrowTractor(models.Model):
	number = models.CharField(max_length=100, blank=True, null=True)
	date = models.CharField(max_length=100, blank=True, null=True)
	from_time = models.CharField(max_length=100, blank=True, null=True)
	to_time = models.CharField(max_length=100, blank=True, null=True)
	quantity = models.CharField(max_length=100, blank=True, null=True)
	fullfilled = models.CharField(max_length=100, blank=True, null=True)

class Location(models.Model):
	lat = models.CharField(max_length=100, blank=True, null=True)
	lng = models.CharField(max_length=100, blank=True, null=True)	

class Crop(models.Model):
	mintemp = models.CharField(max_length=100, blank=True, null=True)
	maxtemp = models.CharField(max_length=100, blank=True, null=True)
	name = models.CharField(max_length=100, blank=True, null=True)
	def __str__(self):
		return self.name

