from django.contrib import admin

# Register your models here.
from pols.models import Question
from pols.models import Choice

admin.site.register(Question)
admin.site.register(Choice)