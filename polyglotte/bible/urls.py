from django.urls import path

from . import views

app_name = 'bible'
urlpatterns = [
    path('', views.HomeView.as_view(), name='home'),
    path('<str:book>/<int:chapter>', views.VersesList.as_view(), name='list'),
    path('<str:book>/<int:chapter>/<int:verse>',
         views.VerseUpdate.as_view(), name='update'),
]
