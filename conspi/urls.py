from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('country/<int:country_id>', views.country, name='country'),
    path('question/<int:question_id>', views.question, name='question'),
]
