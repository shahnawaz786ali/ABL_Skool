from django.shortcuts import render, redirect
from django.http import HttpResponse, HttpResponseRedirect
from django.contrib import messages
from django.urls import reverse 
from django.contrib.auth.decorators import login_required
from curriculum.models import *
from users.models import *
from curriculum import views
from django.core.cache import cache
from django.contrib.admin.models import LogEntry
import datetime as dt
from .signals import succesful_logout
# from reportlab.pdfgen import canvas

def school_home(request,subject_id=None):
    user=request.user
    school=User.objects.get(username=user)
    school_obj = user_profile_school.objects.get(user=school)
    
    school=school_obj.school_name
    students=user_profile_student.objects.filter(school__icontains=school).count()
    teachers=user_profile_teacher.objects.filter(school=school).count()

    subjects=Subject.objects.all().count()

    unread_notifications = NotificationSchool.objects.filter(school_id=school_obj, read=False).count()

    context={
        "total_student": students,
        "profile":school_obj,
        "unread_notifications":unread_notifications,
        "teachers":teachers,
        "subjects":subjects
    }
    return render(request, "school/school_home_template.html", context)


def student_data_view(request):
    return render(request, 'school/student_view_attendance.html')

def student_view_data_post(request):
    if request.method != "POST":
        messages.error(request, "Invalid Method")
        return redirect('users:attendance_data')
    else:
        # Getting all the Input Data
        grade= request.POST.get('grade')

        student_obj = user_profile_student.objects.filter(grade__iexact=grade)
        total_students=student_obj.count()

        context = {
            "student_obj": student_obj,
            "total_students":total_students
        }
        return render(request, 'school/student_data_gradewise.html', context)
    
def display_teachers(request):
    user=request.user
    school=User.objects.get(username=user)
    school_obj = user_profile_school.objects.get(user=school)
    
    school=school_obj.school_name
    teachers=user_profile_teacher.objects.filter(school=school)

    return render(request, "school/teachers_list.html", {"teachers":teachers})

def subject_list(request):
    subjects=Subject.objects.all()

    return render(request, "school/subjects_list.html", {"subjects":subjects})

def school_feedback(request):
    school_obj = user_profile_school.objects.get(user=request.user)
    feedback_data = FeedBackSchool.objects.filter(school=school_obj)
    context = {
        "feedback_data": feedback_data
    }
    return render(request, 'school/school_feedback.html', context)

def school_feedback_save(request):
    if request.method != "POST":
        messages.error(request, "Invalid Method.")
        return redirect('users:school_feedback')
    else:
        feedback = request.POST.get('feedback_message')
        school_obj = user_profile_school.objects.get(user=request.user)

        try:
            add_feedback = FeedBackSchool(school=school_obj, feedback=feedback, feedback_reply="")
            add_feedback.save()
            # messages.success(request, "Feedback Sent.")
            return redirect('users:school_feedback')
        except:
            messages.error(request, "Failed to Send Feedback.")
            return redirect('users:school_feedback')
        
def notifications(request):
    user=request.user
    school=user_profile_school.objects.get(user=user)
    notifications = NotificationSchool.objects.filter(school_id=school).order_by('-id')
    return render(request, 'school/notification.html', {'notifications': notifications})

def mark_notification_as_read(request, id):
    notification = NotificationSchool.objects.get(id=id)
    notification.read = True
    notification.save()
    return redirect('users:school_feedback')

def leaderboard(request):
    students=user_profile_student.objects.order_by('-marks_obtained')[:5]
    return render(request, 'school/leadership.html',{'students':students})

def student_report(request):
    return render(request, "school/student_report.html")

def student_report_gradewise(request):
    if request.method != "POST":
        messages.error(request, "Invalid Method")
        return redirect('users:student_report')
    else:
        # Getting all the Input Data
        grade= request.POST.get('grade')

        student_obj = user_profile_student.objects.filter(grade__iexact=grade)

        context = {
            "student_obj": student_obj,
        }
        return render(request, 'school/student_report_gradewise.html', context)
    
def student_detail_report(request,user_id):
    users=user_profile_student.objects.get(user_id=user_id)
    marks=Topicwise_Marks.objects.filter(student=users)
    return render(request, "school/details_mark.html",{"users":users,"marks":marks})