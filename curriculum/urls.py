from django.urls import path,include
from . import views
from rest_framework.response import Response
from rest_framework import routers

app_name='curriculum'
urlpatterns = [
    path('training_level/',views.training_level, name="training_level"),
    path('trainer_subject_1/',views.trainer_subject_1, name="trainer_subject_1"),
    path('trainer_subject_2/',views.trainer_subject_2, name="trainer_subject_2"),
    path('trainer_subject_3/',views.trainer_subject_3, name="trainer_subject_3"),
    path('trainer_lesson/<slug:slug>',views.trainer_lesson,name="trainer_lesson"),
    path("trainer_lesson_detail/<slug:slug>",views.trainer_lesson_detail, name="trainer_lesson_detail"),
    path('coding/', views.coding, name="coding"),
    path('codinglessons/<slug:slug>/',views.codinglessons,name="codinglessons"),
    path('codinglesson_detail/<slug:slug>/',views.codinglesson_detail, name="codinglesson_detail"),
    path('ai/',views.ai,name="ai"),
    path('lessons/<slug:slug>/',views.lessons,name="lessons"),
    path('lesson_detail/<slug:slug>/',views.lesson_detail, name="lesson_detail"),
    path('', views.StandardListView.as_view(), name='standard_list'),
    path('<slug:slug>/', views.SubjectListView.as_view(), name='subject_list'),
    path('<str:standard>/<slug:slug>/', views.LessonListView.as_view(), name='lesson_list'),
    path('<str:standard>/<str:subject>/<slug:slug>/', views.LessonDetailView.as_view(),name='lesson_detail'),
    path('<str:standard>/<str:slug>/create/', views.LessonCreateView.as_view(),name='lesson_create'),
    path('<str:standard>/<str:subject>/<slug:slug>/update/', views.LessonUpdateView.as_view(),name='lesson_update'),
    path('<str:standard>/<str:subject>/<slug:slug>/delete/', views.LessonDeleteView.as_view(),name='lesson_delete'),
]