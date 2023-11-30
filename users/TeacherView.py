from django.shortcuts import render, redirect
from django.http import HttpResponse, HttpResponseRedirect,JsonResponse
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
from assessment.models import *
from django.db.models import Q,Max
from django.core.exceptions import ObjectDoesNotExist

def teacher_home(request,subject_id=None):
    teacher_obj = user_profile_teacher.objects.get(user=request.user)
    
    school=teacher_obj.school
    students=user_profile_student.objects.filter(school__icontains=school).count()

    subjects=Subject.objects.all().count()

    unread_notifications = NotificationTeacher.objects.filter(teacher_id=teacher_obj, read=False).count()

    context={
        "total_student": students,
        "school":teacher_obj,
        "unread_notifications":unread_notifications,
        "subjects":subjects
    }
    return render(request, "teacher_template/teacher_home_template.html", context)


def subject_list(request):
    subjects={"Python": "7, 8, 9, and 10",
        "AI": "11 and 12",
        "Arduino": "10 and 11",
        "Robotics": "12"}

    return render(request, "teacher_template/subjects_list.html", {"subjects":subjects})

def teacher_feedback(request):
    teacher_obj = user_profile_teacher.objects.get(user=request.user)
    feedback_data = FeedBackTeacher.objects.filter(teacher=teacher_obj)
    context = {
        "feedback_data": feedback_data,
        "school":teacher_obj
    }
    return render(request, 'teacher_template/teacher_feedback.html', context)

def teacher_feedback_save(request):
    if request.method != "POST":
        messages.error(request, "Invalid Method.")
        return redirect('users:teacher_feedback')
    else:
        feedback = request.POST.get('feedback_message')
        teacher_obj = user_profile_teacher.objects.get(user=request.user)

        try:
            add_feedback = FeedBackTeacher(teacher=teacher_obj, feedback=feedback, feedback_reply="")
            add_feedback.save()
            # messages.success(request, "Feedback Sent.")
            return redirect('users:teacher_feedback')
        except:
            messages.error(request, "Failed to Send Feedback.")
            return redirect('users:teacher_feedback')
        
def notifications(request):
    user=request.user
    teacher=user_profile_teacher.objects.get(user=user)
    notifications = NotificationTeacher.objects.filter(teacher_id=teacher).order_by('-id')
    return render(request, 'teacher_template/notification.html', {'notifications': notifications,"school":teacher})

def mark_notification_as_read(request, id):
    notification = NotificationTeacher.objects.get(id=id)
    notification.read = True
    notification.save()
    return redirect('users:teacher_feedback')


def leaderboard(request):
    teacher=user_profile_teacher.objects.get(user=request.user)
    grade=teacher.grade
    
    max_results = Result.objects.values('user__user_profile_student__grade').annotate(max_score=Max('score'))
    overall_students=Result.objects.all().order_by('-score')[:5]

    # Initialize a dictionary to store top 3 students for each grade
    top_students_by_grade = {}

    # Iterate through each grade and get the top 3 students
    for grade_info in max_results:
        grade = grade_info['user__user_profile_student__grade']
        max_score = grade_info['max_score']
        
        # Get the top 3 students with the maximum score in each grade
        top_students = Result.objects.filter(
            user__user_profile_student__grade=grade
        ).order_by('-score')[:3]

        # Add the top students to the dictionary
        top_students_by_grade[grade] = top_students

    return render(request, 'teacher_template/leadership.html', {'top_students_by_grade': top_students_by_grade,"overall_students":overall_students,"school":teacher})

def student_report(request):
    teacher=user_profile_teacher.objects.get(user=request.user)
    school_name=teacher.school
    students = user_profile_student.objects.filter(school=school_name)
    grades = Standard.objects.all()

    students_gradewise = []

    for grade in grades:
        students_for_grade = students.filter(grade=grade)
        total_number=len(students_for_grade)
        students_gradewise.append((grade, students_for_grade,total_number))

    search_query = request.GET.get('search', '')
    if search_query:
        students = students.filter(Q(first_name__icontains=search_query) | Q(last_name__icontains=search_query))
        students_gradewise = [] 

    context = {
        "students_gradewise": students_gradewise,
        "students":students,
        "search_query": search_query,
        "school":school_name
    }
    # if request.is_ajax():
    #     students_data = [{'grade': student.grade, 'student_name': student.first_name, 'student_id': student.user_id} for student in students]
    #     return JsonResponse({'students': students_data})
    
    return render(request, 'teacher_template/view_report.html', context)


def student_report_gradewise(request,grade):
    teacher=user_profile_teacher.objects.get(user=request.user)
    school_name=teacher.school
    query = request.GET.get('q')
    students = user_profile_student.objects.filter(grade=grade)
    student_schoolwise=students.filter(school__icontains=school_name).order_by('first_name')

    if query:
        students = students.filter(
            Q(first_name__icontains=query) | Q(last_name__icontains=query) 
        )
    
    context = {
        'grade': grade,
        'students': student_schoolwise,
        "school":teacher,
        'search_query': query
    }
    
    return render(request, 'teacher_template/student_report_gradewise.html', context)

    
def student_detail_report(request,user_id):
    try:
        teacher=user_profile_teacher.objects.get(user=request.user)
        users=user_profile_student.objects.get(user_id=user_id)
        user=User.objects.get(username=users)
        marks=Result.objects.filter(user=user)

        return render(request, "teacher_template/details_mark.html",{"users":users,"marks":marks,"school":teacher})
    except ObjectDoesNotExist:
        # Handle the case when a matching object doesn't exist
        return HttpResponse("The requested data does not exist.")


def teacher_profile(request):
    user = User.objects.get(id=request.user.id)
    school = user_profile_teacher.objects.get(user=user)

    context={
        "user": user,
        "school": school
    }
    return render(request, 'teacher_template/teacher_profile.html', context)

def teacher_profile_update(request):
    if request.method != "POST":
        messages.error(request, "Invalid Method!")
        return redirect('users:teacher_profile')
    else:
        first_name=request.POST.get('first_name')
        last_name=request.POST.get('last_name')
        school_name = request.POST.get('school_name')
        password = request.POST.get('password')
        mobile= request.POST.get('mobile')
        grade=request.POST.get('grade')
        # profile_pic = request.FILES.get('logo')

        try:
            customuser = User.objects.get(id=request.user.id)
            if password != None and password != "":
                customuser.set_password(password)
            customuser.save()

            teacher = user_profile_teacher.objects.get(user=customuser.id)
            teacher.school=school_name
            teacher.mobile=mobile
            teacher.first_name=first_name
            teacher.last_name=last_name
            teacher.grade=grade
            # school.profile_pic=profile_pic
            teacher.save()
            messages.success(request, "Profile Updated Successfully")
            return redirect('users:teacher_profile')
        except:
            messages.error(request, "Failed to Update Profile")
            return redirect('users:teacher_profile')