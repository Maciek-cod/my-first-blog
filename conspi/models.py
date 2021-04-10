from django.db import models
from django import forms
from django.forms import ModelForm

# Create your models here.
class Country(models.Model):
	name = models.CharField(max_length=50)

	def __str__(self):
		return self.name

	class Meta:
		verbose_name_plural = "Countries"

class Question(models.Model):
	title = models.TextField(max_length=200)

	def __str__(self):
		return str(self.pk) +": "+ self.title

	class Meta:
		verbose_name_plural = "Question"

class Answer(models.Model):

	country = models.ForeignKey(Country, on_delete=models.CASCADE)
	question = models.ForeignKey(Question, on_delete=models.CASCADE)
	unweight_base = models.CharField(max_length=50)
	base = models.CharField(max_length=50)
	defenetely_true = models.CharField(max_length=50)
	probably_true = models.CharField(max_length=50)
	probably_false = models.CharField(max_length=50) 
	defenetely_false = models.CharField(max_length=50)
	dont_know = models.CharField(max_length=50)

	def __str__(self):
		return str(self.pk) + " " + str(self.country) + ": " + str(self.question) + " = " + str(self.probably_false)

	class Meta:
		verbose_name_plural = "Answer"

