from django.shortcuts import render
from django.views import View
from notes_app.models import Diary, Category
import datetime

# Create your views here.

def get_all_entries():
    entries = list(Diary.objects.all())
    formattedEntries = []
    for i in entries:
        formattedEntries.append((i.note, i.date_time_issued.strftime("%A"),
                                 i.date_time_issued.strftime("%x"),
                                 i.date_time_issued.strftime("%H:%M"), i.category))
    return formattedEntries

class Home(View):
    def get(self, request):
        print(get_all_entries())
        return render(request, 'index.html', {"message": get_all_entries()})


    def post(self, request):
        print(request.POST)
        try:
            note = request.POST["note"]
            print(type(request.POST["date_issued"]))
            newDate = datetime.datetime.strptime(request.POST["date_issued"], '%Y-%m-%dT%H:%M')
            print(type(newDate))
            category = request.POST["category"]
            category_instance = Category.objects.create(name=category)
            Diary.objects.create(note=note, date_time_issued=newDate, day= newDate.strftime("%A"), category=category_instance)
            user_message = "note added successfully"

        except ValueError:
            user_message = "you didn't enter the details correctly"

        return render(request, 'response.html', {"message": get_all_entries(), "user_message": user_message})


class History(View):
    def get(self, request):
        return render(request, 'history.html')


    def post(self, request):
        print(request.POST)

        entries = list(Diary.objects.filter(day=request.POST['days'], category__name=request.POST['category']))
        print(entries)

        formattedEntries = []
        for i in entries:
            formattedEntries.append((i.note,
                                     i.date_time_issued.strftime("%x"),
                                     i.date_time_issued.strftime("%H:%M")))

        return render(request, 'history.html', {"message": formattedEntries})