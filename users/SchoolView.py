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
from reportlab.pdfgen import canvas

def school_home(request,subject_id=None):
    global absent_count
    global count_present 

    user=request.user
    student=User.objects.get(username=user)
    student_obj = user_profile_student.objects.get(user=student)
    
    school=student_obj.school
    students=user_profile_student.objects.filter(school__icontains=school).count()
    # print(students)
    teachers=user_profile_teacher.objects.filter(school=school).count()

    subjects=Subject.objects.all().count()
    
    ct=cache.get('count', version=user.username)
    total_attendance = AttendanceReport.objects.filter(user=student_obj).count()
    attendance_present = AttendanceReport.objects.filter(user=student_obj, status=True).count()
    attendance_absent = AttendanceReport.objects.filter(user=student_obj, status=False).count()

    student_grade = Standard.objects.get(id=student_obj.grade)
    total_subjects = Subject.objects.filter(standard_id=student_grade).count()

    subject_name = []
    data_present = []
    data_absent = []
    subject_data = Subject.objects.filter(standard_id=student_grade)
    for subject in subject_data:
        attendance = Attendance.objects.filter(id=subject.id)
        attendance_present_count = AttendanceReport.objects.filter(attendance_id__in=attendance, status=True,user=student_obj).count()
        attendance_absent_count =0
        subject_name.append(subject.name)
        data_present.append(attendance_present_count)
        data_absent.append(attendance_absent_count)

    logs=LogEntry.objects.all()

    for l in logs:
        actionTime=l.action_time

    count_absent=cache.get('absent', version=user.username)
    present_count=cache.get('present', version=user.username)

    unread_notifications = NotificationStudent.objects.filter(student_id=student_obj, read=False).count()

    context={
        "total_student": students,
        "attendance_present": present_count,
        "attendance_absent": count_absent,
        "total_subjects": total_subjects,
        "subject_name": subject_name,
        "data_present": data_present,
        "data_absent": data_absent,
        "profile":student_obj,
        "recent_visit":actionTime,
        "unread_notifications":unread_notifications,
        "teachers":teachers,
        "subjects":subjects
    }
    return render(request, "school/school_home_template.html", context)

# def student_gradewise(request):
#     user=request.user
#     student = user_profile_student.objects.get(user=request.user.id) 
#     school=student.school
#     students=user_profile_student.objects.filter(school__icontains=school)
#     # print(students)
#     # Getting Logged in Student Data
#     course = student.grade # Getting Course Enrolled of LoggedIn Student
#     subjects = Subject.objects.filter(standard=course) # Getting the Subjects of Course Enrolled
#     context = {
#         "students": students
#     }
#     return render(request, "school/student_view_attendance.html", context)

def student_data_view(request):
    return render(request, 'school/student_view_attendance.html')

def student_view_data_post(request):
    if request.method != "POST":
        messages.error(request, "Invalid Method")
        return redirect('users:attendance_data')
    else:
        # Getting all the Input Data
        grade= request.POST.get('grade')

        student_obj = user_profile_student.objects.filter(grade__icontains=grade)

        context = {
            "student_obj": student_obj,
        }
        return render(request, 'school/student_data_gradewise.html', context)
    
def display_teachers(request):
    user=request.user
    school=User.objects.get(username=user)
    school_obj = user_profile_student.objects.get(user=school)
    
    school=school_obj.school
    teachers=user_profile_teacher.objects.filter(school=school)

    return render(request, "school/teachers_list.html", {"teachers":teachers})

def subject_list(request):
    subjects=Subject.objects.all()

    return render(request, "school/subjects_list.html", {"subjects":subjects})