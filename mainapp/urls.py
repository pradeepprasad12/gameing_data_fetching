from django.urls import path
from . import views

urlpatterns = [
    path('', views.matches_view, name='matches_view'),
    path('squads/<int:competition_id>/', views.squads_view, name='squads_view'),
]
