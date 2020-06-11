from django.urls import path
from . import views
urlpatterns = [
	path('home/', views.home, name="home"),
	path('home/schools/', views.schools),
	path('home/postgraduate/', views.postgrad),
	path('home/professional/', views.professional),
	path('home/schools/deadlines/', views.deadlines, name='deadlines')
]
