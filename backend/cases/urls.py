from django.urls import path
from . import views

urlpatterns = [
    path('', views.case_list, name='case-list'),
    path('<int:case_id>/', views.case_detail, name='case-detail'),
    path('clues/', views.clue_list_create, name='clue-list-create'),
    path('clues/<int:clue_id>/', views.clue_delete, name='clue-delete'),

    path('my/', views.my_cases, name='my-cases'),
    path('<int:case_id>/collaborators/', views.case_collaborators, name='case-collaborators'),
    path('<int:case_id>/collaborators/<int:collaborator_id>/', views.remove_collaborator, name='remove-collaborator'),

    # ↓ YANGI
    path('<int:case_id>/edit/', views.case_edit, name='case-edit'),
    path('<int:case_id>/publish/', views.case_publish, name='case-publish'),
    path('<int:case_id>/scenes/', views.scene_list_create, name='scene-list-create'),
    path('<int:case_id>/scenes/<int:scene_id>/', views.scene_detail_edit, name='scene-detail-edit'),
    path('<int:case_id>/characters/', views.character_list_create, name='character-list-create'),
    path('<int:case_id>/characters/<int:character_id>/', views.character_detail_edit, name='character-detail-edit'),
]