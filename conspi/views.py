from django.utils import timezone
from django.shortcuts import render, get_object_or_404
from django.shortcuts import redirect
from .models import Country, Question, Answer
from django.http import HttpResponse

from django import forms

class MacForm(forms.Form):
    country = forms.ModelChoiceField(queryset=Country.objects.all().order_by('id'), empty_label="Choose")
    question = forms.ModelChoiceField(queryset=Question.objects.all().order_by('id'), empty_label="Choose")
    FLOW_CHOICES = (
        ("-","Descendingly"),
        ("+","Ascendingly"),
    )
    flow = forms.ChoiceField(choices = FLOW_CHOICES)

def home(request):
    print("Dostalem request: " , request)
    print(dir(request))
    print(request.GET)
    print(request.POST)
    print(request.body)
    countries = Country.objects.all().order_by('id') # ('-id')
    questions = Question.objects.all().order_by('id')
    the_country = None
    the_question = None
    answer = None
    an_def_t = []
    an_pro_t = []
    an_pro_f = []
    an_def_f = []
    an_do_kn = []

    if request.method == "POST":

        form = MacForm(request.POST)
        
        if form.is_valid():

            country_name = form.cleaned_data['country']
            question = form.cleaned_data['question']
            upordown = form.cleaned_data['flow']
            if upordown == "+":
                upordown=""
        
            the_country = Country.objects.get(name=country_name)
            the_question = Question.objects.get(id=question.id)
            answer = Answer.objects.filter(country=country_name, question=question)
            an_def_t = Answer.objects.filter(question=question).order_by(upordown + 'definitely_true')
            an_pro_t = Answer.objects.filter(question=question).order_by(upordown + 'probably_true')
            an_pro_f = Answer.objects.filter(question=question).order_by(upordown + 'probably_false')
            an_def_f = Answer.objects.filter(question=question).order_by(upordown + 'definitely_false')
            an_do_kn = Answer.objects.filter(question=question).order_by(upordown + 'dont_know')

    else:
        form = MacForm()

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
            'form':form,
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

    previous = question_id - 1
    nextt = question_id + 1
    if question_id == 9:
        nextt = 1
    if question_id == 1:
        previous = 9
    
    context = {
        'previous':previous,
        'nextt':nextt,
        'answers':answers,
        'question':question,
    }
    return render(request, 'conspi/question.html', context=context)

