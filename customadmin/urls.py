from django.urls import path
from . import views
from users.models import *

urlpatterns = [
    path('',views.signup_admin, name="signup_admin"),
    path('admin_home/',views.admin_home, name="admin_home"),
    path('add_grade',views.add_grade,name="add_grade"),
    path('add_grade_save',views.add_grade_save,name="add_grade_save"),
    path('manage_grade', views.manage_grade,name="manage_grade"),
    path('edit_grade/<int:grade_id>',views.edit_grade,name="edit_grade"),
    path('edit_grade_save',views.edit_grade_save,name="edit_grade_save"),
    path('add_subject', views.add_subject,name="add_subject"),
    path('add_subject_save', views.add_subject_save,name="add_subject_save"),
    path('manage_subject', views.manage_subject,name="manage_subject"),
    path('edit_subject/<str:subject_id>', views.edit_subject,name="edit_subject"),
    path('edit_subject_save', views.edit_subject_save,name="edit_subject_save"),
    path('add_lesson', views.add_lesson,name="add_lesson"),
    path('add_lesson_save', views.add_lesson_save,name="add_lesson_save"),
    path('add_student', views.add_student,name="add_student"),
    path('add_student_save', views.add_student_save,name="add_student_save"),
    path("manage_lesson",views.manage_lesson, name="manage_lesson"),
    path("edit_lesson/<str:lesson_id>",views.edit_lesson,name="edit_lesson"),
    path("edit_lesson_save",views.edit_lesson_save,name="edit_lesson_save"),
]