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
        "school":school_obj,
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
    subjects={"Python": "7, 8, 9, and 10",
        "AI": "11 and 12",
        "Arduino": "10 and 11",
        "Robotics": "12"}

    return render(request, "school/subjects_list.html", {"subjects":subjects})

def school_feedback(request):
    school_obj = user_profile_school.objects.get(user=request.user)
    feedback_data = FeedBackSchool.objects.filter(school=school_obj)
    context = {
        "feedback_data": feedback_data,
        "school":school_obj
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
    return render(request, 'school/notification.html', {'notifications': notifications,"school":school})

def mark_notification_as_read(request, id):
    notification = NotificationSchool.objects.get(id=id)
    notification.read = True
    notification.save()
    return redirect('users:school_feedback')


def leaderboard(request):
    school=user_profile_school.objects.get(user=request.user)
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

    return render(request, 'school/leadership.html', {'top_students_by_grade': top_students_by_grade,"overall_students":overall_students,"school":school})

def student_report(request):
    school=user_profile_school.objects.get(user=request.user)
    students = user_profile_student.objects.all()
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
        "school":school
    }
    if request.is_ajax():
        students_data = [{'grade': student.grade, 'student_name': student.first_name, 'student_id': student.user_id} for student in students]
        return JsonResponse({'students': students_data})
    
    return render(request, 'school/view_report.html', context)


def student_report_gradewise(request,grade):
    school=user_profile_school.objects.get(user=request.user)
    query = request.GET.get('q')
    students = user_profile_student.objects.filter(grade=grade)

    if query:
        students = students.filter(
            Q(first_name__icontains=query) | Q(last_name__icontains=query) 
        )
    
    context = {
        'grade': grade,
        'students': students,
        "school":school,
        'search_query': query
    }
    
    return render(request, 'school/student_report_gradewise.html', context)

# def student_report_gradewise(request):
#     if request.method != "POST":
#         messages.error(request, "Invalid Method")
#         return redirect('users:student_report')
#     else:
#         grade= request.POST.get('grade')
#         student_name = request.POST.get("student_name")

#         student_obj = user_profile_student.objects.filter(grade__iexact=grade)

#         context = {
#             "student_obj": student_obj,
#         }
#         return render(request, 'school/student_report_gradewise.html', context)
    
def student_detail_report(request,user_id):
    try:
        school=user_profile_school.objects.get(user=request.user)
        users=user_profile_student.objects.get(user_id=user_id)
        user=User.objects.get(username=users)
        marks=Result.objects.filter(user=user)

        return render(request, "school/details_mark.html",{"users":users,"marks":marks,"school":school})
    except ObjectDoesNotExist:
        # Handle the case when a matching object doesn't exist
        return HttpResponse("The requested data does not exist.")


def school_profile(request):
    user = User.objects.get(id=request.user.id)
    school = user_profile_school.objects.get(user=user)

    context={
        "user": user,
        "school": school
    }
    return render(request, 'school/school_profile.html', context)

def school_profile_update(request):
    if request.method != "POST":
        messages.error(request, "Invalid Method!")
        return redirect('users:school_profile')
    else:
        school_name = request.POST.get('school_name')
        principal_name = request.POST.get('principal_name')
        password = request.POST.get('password')
        mobile= request.POST.get('mobile')
        country= request.POST.get('country')
        state= request.POST.get('state')
        city= request.POST.get('city')
        district=request.POST.get('district')
        street=request.POST.get('street')
        pincode=request.POST.get('pincode')
        mentor=request.POST.get('mentor')
        logo = request.FILES.get('logo')

        try:
            customuser = User.objects.get(id=request.user.id)
            if password != None and password != "":
                customuser.set_password(password)
            customuser.save()

            school = user_profile_school.objects.get(user=customuser.id)
            school.school_name=school_name
            school.principal=principal_name
            school.mentor=mentor
            school.mobile=mobile
            school.country=country
            school.state=state
            school.city=city
            school.district=district
            school.pin=pincode
            school.street=street
            school.logo=logo
            school.save()
            messages.success(request, "Profile Updated Successfully")
            return redirect('users:school_profile')
        except:
            messages.error(request, "Failed to Update Profile")
            return redirect('users:school_profile')