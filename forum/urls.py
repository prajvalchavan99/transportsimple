from django.urls import path
from . import views

app_name = 'forum'

urlpatterns = [
    path('questions/', views.question_list_view, name='question_list'),
    path('questions/<int:pk>/', views.question_detail_view, name='question_detail'),
    path('ask/', views.ask_question_view, name='ask_question'),
    path('questions/<int:pk>/answer/', views.answer_question_view, name='answer_question'),
    path('like/<int:answer_id>/', views.like_answer_view, name='like_answer'),
]
