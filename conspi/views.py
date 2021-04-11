from django.utils import timezone
from django.shortcuts import render, get_object_or_404
from django.shortcuts import redirect
from .models import Country, Question, Answer
from django.http import HttpResponse


def home(request):
	print("Dostalem request: " , request)
	print(dir(request))
	print(request.GET)
	print(request.POST)
	print(request.body)
	countries = Country.objects.all().order_by('id') # ('-id')
	questions = Question.objects.all().order_by('id')

	if request.method == "POST":

		country_id = request.POST['country']
		question_id = request.POST['question']
		upordown = request.POST['upordown']
		
		the_country = Country.objects.get(pk=country_id)
		the_question = Question.objects.get(pk=question_id)
		answer = Answer.objects.filter(country=country_id, question=question_id)
		an_def_t = Answer.objects.filter(question=question_id).order_by(upordown + 'definitely_true')
		an_pro_t = Answer.objects.filter(question=question_id).order_by(upordown + 'probably_true')
		an_pro_f = Answer.objects.filter(question=question_id).order_by(upordown + 'probably_false')
		an_def_f = Answer.objects.filter(question=question_id).order_by(upordown + 'definitely_false')
		an_do_kn = Answer.objects.filter(question=question_id).order_by(upordown + 'dont_know')
		context = {
			'countries':countries,
			'questions':questions,
			'the_country':the_country,
			'the_question':the_question,
			'answer':answer,
			'an_def_f':an_def_f,
			'an_pro_t':an_pro_t,
			'an_def_t':an_def_t,
			'an_pro_f':an_pro_f,
			'an_do_kn':an_do_kn,
		}
		return render(request, 'conspi/home.html', context=context)
	context = {
		'countries':countries,
		'questions':questions,
	}
	return render(request, 'conspi/home.html', context=context)

def country(request, country_id):
	countries = Country.objects.all().order_by('id').exclude(id=country_id)
	country = get_object_or_404(Country, pk=country_id)
	answers = Answer.objects.filter(country=country_id)
	context = {
		'country':country,
		'answers':answers,
		'countries':countries,
	}
	return render(request, 'conspi/country.html', context=context)

def question(request, question_id):
	answers = Answer.objects.filter(question=question_id)
	question = get_object_or_404(Question, pk=question_id)
	context = {
		'answers':answers,
		'question':question,
	}
	return render(request, 'conspi/question.html', context=context)

