from django.urls import path
from pols.views import index

urlpatterns = [
	path('index/',index, name="Hello, world. You're at the polls index."),
]