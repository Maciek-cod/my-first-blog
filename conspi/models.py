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
	title = models.CharField(max_length=200)

	def __str__(self):
		return str(self.pk)

	class Meta:
		verbose_name_plural = "Question"

class Answer(models.Model):

	country = models.ForeignKey(Country, on_delete=models.CASCADE)
	question = models.ForeignKey(Question, on_delete=models.CASCADE)
	unweight_base = models.CharField(max_length=50)
	base = models.IntegerField()
	definitely_true = models.IntegerField()
	probably_true = models.IntegerField()
	probably_false = models.IntegerField()
	definitely_false = models.IntegerField()
	dont_know = models.IntegerField()

	def __str__(self):
		return str(self.pk) + " " + str(self.country) + ": " + str(self.question) + " = " + str(self.probably_false)

	class Meta:
		verbose_name_plural = "Answer"

