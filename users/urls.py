from django.urls import path,include
from . import views
from django.contrib.auth import views as auth_views
from users.utils import activate
from .editor_views import *
from . import StudentViews
from . import SchoolView, PrincipalView,TeacherView

urlpatterns = [
    path('', views.index, name="index"),
    path('contact/', views.contact, name="contact"),
    path('student/', views.StudentSignUpView.as_view(), name="user_student"),
    path('parent/', views.ParentSignUpView.as_view(), name="user_parent"),
    path('teacher/', views.TeacherSignUpView.as_view(), name="user_teacher"),
    path('principal/', views.PrincipalSignUpView.as_view(), name="user_principal"),
    path('school/', views.SchoolSignUpView.as_view(), name="user_school"),
    path('login/',views.user_login, name="login"),
    path('payment/', views.payment, name='payment'),
    path('payment_view/', views.payment_view, name='payment_view'),
    path('account/login/',views.user_login, name="login"),
    path('logout/', views.user_logout, name='user_logout'),
    path('register/', views.register, name='register'),
    path('student_report/',views.studentreport, name="student_report"),
    path('book-demo/', views.book_demo, name='book_demo'),
    path('success/', views.success_page, name='success_page'),
    path('create_student_project/', views.create_student_project, name='create_student_project'),
    path('reset_password/', auth_views.PasswordResetView.as_view(
                    template_name="registration/password_reset.html"
    ),name="reset_password"),
    path('reset_password_sent',auth_views.PasswordResetDoneView.as_view(template_name="registration/password_reset_done.html"),name="pasword_reset_done"),
    path('reset/<uidb64>/<token>/',auth_views.PasswordResetConfirmView.as_view(template_name="registration/password_reset_confirm.html"),name="password_reset_confirm"),
    path('reset_password_complete/',auth_views.PasswordResetCompleteView.as_view(template_name="registration/password_reset_complete.html"),name="password_reset_complete"),
    path('editor/',views.editor, name="editor"),
    path('editor_index/',views.editor_index, name="editor_index"),
    path('activate/<uidb64>/<token>/',activate, name="activate"),
    path('home/',greetings,name="greetings"),
    path('home/run',runcode,name="runcode"),
    # path('student_profile/',student_home, name="student_dashboard"),
    path('enquiry',views.enquiry, name="enquiry"),
    path('message',views.message, name="message"),
    
    # URSL for Student
    path('student_home/', StudentViews.student_home, name="student_home"),
    path('student_view_attendance/', StudentViews.student_view_attendance, name="student_view_attendance"),
    path('student_view_attendance_post/', StudentViews.student_view_attendance_post, name="student_view_attendance_post"),
    path('student_feedback/', StudentViews.student_feedback, name="student_feedback"),
    path('student_feedback_save/', StudentViews.student_feedback_save, name="student_feedback_save"),
    path('student_profile/', StudentViews.student_profile, name="student_profile"),
    path('student_profile_update/', StudentViews.student_profile_update, name="student_profile_update"),
    path('student_view_result/', StudentViews.student_report, name="student_view_result"),
    path('student_certificate/', StudentViews.generate_certificate, name="student_certificate"),
    path('getsubject/', StudentViews.getsubject, name="getsubject"),
    path('notification/', StudentViews.notifications, name="notification"),
    path('notification_read/<int:id>/', StudentViews.mark_notification_as_read, name="notification_read"),
    path("student_leaderboard/",StudentViews.leaderboard, name="student_leaderboard"),
    path("subjects/",StudentViews.subjects, name="subjects"),

    # URLS for School
    path('school_home/', SchoolView.school_home, name="school_home"),
    path('attendance_data/', SchoolView.student_data_view, name="attendance_data"),
    path('attendance_data_post/', SchoolView.student_view_data_post, name="attendance_data_post"),
    path('teachers_list/', SchoolView.display_teachers, name="teachers_list"),
    path('subject_list/', SchoolView.subject_list, name="subject_list"),
    path('school_profile/', SchoolView.school_profile, name="school_profile"),
    path('school_profile_update/', SchoolView.school_profile_update, name="school_profile_update"),
    path('school_feedback/', SchoolView.school_feedback, name="school_feedback"),
    path('school_feedback_save/', SchoolView.school_feedback_save, name="school_feedback_save"),
    path('school_notification/', SchoolView.notifications, name="school_notification"),
    path('school_notification_read/<int:id>/', SchoolView.mark_notification_as_read, name="school_notification_read"),
    path("leaderboard/",SchoolView.leaderboard, name="leaderboard"),
    path("student_report", SchoolView.student_report, name="student_report"),
    path("student_report_gradewise/<str:grade>/", SchoolView.student_report_gradewise, name="student_report_gradewise"),
    path("student_detail_report/<user_id>", SchoolView.student_detail_report, name="student_detail_report"),

    # URLS for principal
    path('principal_home/', PrincipalView.principal_home, name="principal_home"),
    path('attendance_data/', PrincipalView.student_data_view, name="attendance_data"),
    path('attendance_data_post/', PrincipalView.student_view_data_post, name="attendance_data_post"),
    path('pteachers_list/', PrincipalView.display_teachers, name="pteachers_list"),
    path('psubject_list/', PrincipalView.subject_list, name="psubject_list"),
    path('principal_profile/', PrincipalView.school_profile, name="principal_profile"),
    path('principal_profile_update/', PrincipalView.school_profile_update, name="principal_profile_update"),
    path('principal_feedback/', PrincipalView.school_feedback, name="principal_feedback"),
    path('principal_feedback_save/', PrincipalView.school_feedback_save, name="principal_feedback_save"),
    path('principal_notification/', PrincipalView.notifications, name="principal_notification"),
    path('principal_notification_read/<int:id>/', PrincipalView.mark_notification_as_read, name="principal_notification_read"),
    path("pleaderboard/",PrincipalView.leaderboard, name="pleaderboard"),
    path("pstudent_report", PrincipalView.student_report, name="pstudent_report"),
    path("pstudent_report_gradewise/<str:grade>/", PrincipalView.student_report_gradewise, name="pstudent_report_gradewise"),
    path("pstudent_detail_report/<user_id>", PrincipalView.student_detail_report, name="pstudent_detail_report"),


    # URLS for teacher
    path('teacher_home/', TeacherView.teacher_home, name="teacher_home"),
    path('tsubject_list/', TeacherView.subject_list, name="tsubject_list"),
    path('teacher_profile/', TeacherView.teacher_profile, name="teacher_profile"),
    path('teacher_profile_update/', TeacherView.teacher_profile_update, name="teacher_profile_update"),
    path('teacher_feedback/', TeacherView.teacher_feedback, name="teacher_feedback"),
    path('teacher_feedback_save/', TeacherView.teacher_feedback_save, name="teacher_feedback_save"),
    path('teacher_notification/', TeacherView.notifications, name="teacher_notification"),
    path('teacher_notification_read/<int:id>/', TeacherView.mark_notification_as_read, name="teacher_notification_read"),
    path("tleaderboard/",TeacherView.leaderboard, name="tleaderboard"),
    path("tstudent_report", TeacherView.student_report, name="tstudent_report"),
    path("tstudent_report_gradewise/<str:grade>/", TeacherView.student_report_gradewise, name="tstudent_report_gradewise"),
    path("tstudent_detail_report/<user_id>", TeacherView.student_detail_report, name="tstudent_detail_report")
]

from django.conf import settings
from django.conf.urls.static import static

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)