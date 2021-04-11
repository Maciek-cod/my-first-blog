from django.core.management.base import BaseCommand, CommandError
from conspi.models import Country, Question, Answer
from mysite.settings import BASE_DIR
from django.shortcuts import get_object_or_404




class Command(BaseCommand):
    help = 'I am importing data from countries.csv'

    def handle(self, *args, **options): 
        if input("Would you like to upload countries if none?(y/n)") == "y":
            country_counter = len(Country.objects.all())
            if country_counter == 0:
                filename = "countries.csv"
                file = open(BASE_DIR / filename)
                country_counter = 0 
                for line in file.readlines():
                    country_counter += 1
                    line = line.strip()
                    c = Country(name=line)
                    c.save()
                self.stdout.write(self.style.SUCCESS("Succesfully imported %s countries." % country_counter))
            else:
                self.stderr.write("Data here!")
                self.stdout.write("The are %s countries already." % country_counter )
                if input("Would you like to upload countries again from csv file?(y/n)") == "y":
                    filename = "countries.csv"
                    file = open(BASE_DIR / filename)
                    country_counter = 0 
                    for line in file.readlines():
                        country_counter += 1
                        line = line.strip()
                        c = Country(name=line)
                        c.save()
                    self.stdout.write(self.style.SUCCESS("Succesfully imported %s countries." % country_counter))

        if input("Would you like to upload questions if none?(y/n)") == "y":
            questions_counter = len(Question.objects.all())
            if questions_counter == 0:
                filename = "questions.csv"
                file = open(BASE_DIR / filename)
                questions_counter = 0 
                for line in file.readlines():
                    questions_counter += 1
                    line = line.strip()
                    q = Question(title=line)
                    q.save()
                self.stdout.write(self.style.SUCCESS("Succesfully imported %s questions." % questions_counter))
            else:
                self.stderr.write("Data here!")
                self.stdout.write("The are %s questions already." % questions_counter )
                if input("Would you like to upload questions again from csv file?(y/n)") == "y":
                    filename = "questions.csv"
                    file = open(BASE_DIR / filename)
                    questions_counter = 0 
                    for line in file.readlines():
                        questions_counter += 1
                        line = line.strip()
                        q = Question(title=line)
                        q.save()
                    self.stdout.write(self.style.SUCCESS("Succesfully imported %s questions." % questions_counter))


        if input("Would you like to upload answers if none?(y/n)") == "y":
            answers_counter = len(Answer.objects.all())
            if answers_counter == 0:
                filename = "answers.csv"
                file = open(BASE_DIR / filename)
                answers_counter = 0 
                for line in file.readlines():
                    item = line.split(',')
                    answers_counter += 1
                    w = Answer(country = Country.objects.get(pk=int(item[0])),
                        question =  Question.objects.get(pk=int(item[1])),
                        unweight_base = int(item[2]),
                        base = int(item[3]),
                        definitely_true = int(item[4]),
                        probably_true = int(item[5]),
                        probably_false = int(item[6]),
                        definitely_false = int(item[7]),
                        dont_know = int(item[8]))
                    w.save()
                self.stdout.write(self.style.SUCCESS("Succesfully imported %s answers." % answers_counter))
            else:
                self.stderr.write("Data here!")
                self.stdout.write("The are %s answers already." % answers_counter )
                if input("Would you like to upload answers again from csv file?(y/n)") == "y":
                    filename = "answers.csv"
                    file = open(BASE_DIR / filename)
                    answers_counter = 0 
                    for line in file.readlines():
                        item = line.split(',')
                        answers_counter += 1
                        w = Answer(country = Country.objects.get(pk=item[0]),
                        question =  Question.objects.get(pk=item[1]),
                        unweight_base = int(item[2]),
                        base = int(item[3]),
                        defenetely_true = item[4],
                        probably_true = item[5],
                        probably_false = item[6],
                        defenetely_false = item[7],
                        dont_know = item[8])
                        w.save()
                    self.stdout.write(self.style.SUCCESS("Succesfully imported %s answers." % answers_counter))

















            






