from django.urls import path
from . import views

urlpatterns = [
    path('', views.case_list, name='case-list'),
    path('<int:case_id>/', views.case_detail, name='case-detail'),
    path('clues/', views.clue_list_create, name='clue-list-create'),
    path('clues/<int:clue_id>/', views.clue_delete, name='clue-delete'),
]