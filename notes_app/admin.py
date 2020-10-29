from django.contrib import admin
from notes_app.models import Category, Diary
# Register your models here.
admin.site.register(Diary)
admin.site.register(Category)
