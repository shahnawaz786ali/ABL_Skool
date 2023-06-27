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

def student_home(request,subject_id=None):
    global absent_count
    global count_present 

    user=request.user
    student=User.objects.get(username=user)
    student_obj = user_profile_student.objects.get(user=student)
    
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
        "total_attendance": len(logs),
        "attendance_present": present_count,
        "attendance_absent": count_absent,
        "total_subjects": total_subjects,
        "subject_name": subject_name,
        "data_present": data_present,
        "data_absent": data_absent,
        "profile":student_obj,
        "recent_visit":actionTime,
        "unread_notifications":unread_notifications
    }
    return render(request, "student_template/student_home_template.html", context)

def student_view_attendance(request):
    student = user_profile_student.objects.get(user=request.user.id) # Getting Logged in Student Data
    course = student.grade # Getting Course Enrolled of LoggedIn Student
    subjects = Subject.objects.filter(standard=course) # Getting the Subjects of Course Enrolled
    context = {
        "subjects": subjects
    }
    return render(request, "student_template/student_view_attendance.html", context)

def student_view_attendance_post(request):
    if request.method != "POST":
        messages.error(request, "Invalid Method")
        return redirect('users:student_view_attendance')
    else:
        # Getting all the Input Data
        subject_id = request.POST.get('subject')
        start_date = request.POST.get('start_date')
        end_date = request.POST.get('end_date')

        # Parsing the date data into Python object
        start_date_parse = dt.datetime.strptime(start_date, '%Y-%m-%d')
        end_date_parse = dt.datetime.strptime(end_date, '%Y-%m-%d')

        subject_obj = Subject.objects.get(subject_id=subject_id)
        # Getting Logged In User Data
        user_obj = User.objects.get(username=request.user)
        # Getting Student Data Based on Logged in Data
        stud_obj = user_profile_student.objects.get(user=user_obj)

        logs=LogEntry.objects.all()
        present_x=[]

        attendance = Attendance.objects.filter(user=user_obj)

        attendance_reports = AttendanceReport.objects.filter(attendance_id__in=attendance)

        for l in logs:
            if start_date_parse < l.action_time < end_date_parse:
                present_x.append(l.action_time)
                attendance_reports.status=True
            else:
                attendance_reports.status=False

        print(present_x)

        context = {
            "subject_obj": subject_obj,
            "attendance_reports": present_x
        }

        return render(request, 'student_template/student_attendance_data.html', context)


def student_profile(request):
    user = User.objects.get(id=request.user.id)
    student = user_profile_student.objects.get(user=user)

    context={
        "user": user,
        "student": student
    }
    return render(request, 'student_template/student_profile.html', context)


def student_profile_update(request):
    if request.method != "POST":
        messages.error(request, "Invalid Method!")
        return redirect('users:student_profile')
    else:
        first_name = request.POST.get('first_name')
        last_name = request.POST.get('last_name')
        password = request.POST.get('password')
        middle_name= request.POST.get('middle_name')
        dob= request.POST.get('dob')
        grade= request.POST.get('grade')
        school= request.POST.get('school')
        profile_pic=request.POST.get('profile_pic')

        try:
            customuser = User.objects.get(id=request.user.id)
            customuser.first_name = first_name
            customuser.last_name = last_name
            if password != None and password != "":
                customuser.set_password(password)
            customuser.save()

            student = user_profile_student.objects.get(user=customuser.id)
            student.dob=dob
            student.middle_name=middle_name
            student.grade=grade
            student.school=school
            student.profile_pic.url=profile_pic
            student.save()
            messages.success(request, "Profile Updated Successfully")
            return redirect('users:student_profile')
        except:
            messages.error(request, "Failed to Update Profile")
            return redirect('users:student_profile')

def student_view_result(request):
    student = user_profile_student.objects.get(admin=request.user.id)
    student_result = StudentResult.objects.filter(student_id=student.id)
    context = {
        "student_result": student_result,
    }
    return render(request, "student_template/student_view_result.html", context)

def student_report(request):
    student=user_profile_student.objects.get(user=request.user)
    students=StudentResult.objects.filter(student_id=student)
    # subjects=Subject.objects.filter(standard=student.grade)
    # for subject in subjects:
    #     StudentResult.objects.create(student_id=student, subject_id=subject,marks=random.randint(1,20))
    return render(request, 'student_template/studentreport.html', {'students': students})

def generate_certificate(request):
    # Get relevant data (e.g., student name, course name, completion date)
    user=request.user
    student_name =user_profile_student.objects.get(user=user)
    grade =student_name.grade
    subjects=Subject.objects.filter(standard=grade)
    subject=subjects[0]

    # Create a new PDF file
    response = HttpResponse(content_type='application/pdf')
    response['Content-Disposition'] = 'attachment; filename="certificate.pdf"'
    # Create a canvas to draw on
    p = canvas.Canvas(response)
    # Customize the certificate template
    p.setFont("Helvetica", 16)
    p.drawString(100, 750, "Certificate of Completion")
    p.setFont("Helvetica", 12)
    p.drawString(100, 700, f"This certifies that {student_name} of grade {grade}")
    p.drawString(100, 675, f"has successfully completed the assessment")
    # p.drawString(100, 650, f"{grade}")
    p.drawString(100, 625, f"on subject {subject}")

    # Save the canvas contents
    p.showPage()
    p.save()

    return response

def getsubject(request):
    user=User.objects.get(username=request.user)
    student=user_profile_student.objects.get(user=user)
    standard=student.grade
    subjects=Subject.objects.filter(standard=standard)
    lesson=Lesson.objects.filter(subject__in=subjects)
    
    return render(request, "student_template/manage_subject_template.html", {"subjects":subjects, "lesson":lesson, "standard":standard})

def student_feedback(request):
    student_obj = user_profile_student.objects.get(user=request.user)
    feedback_data = FeedBackStudent.objects.filter(student=student_obj)
    context = {
        "feedback_data": feedback_data
    }
    return render(request, 'student_template/student_feedback.html', context)

def student_feedback_save(request):
    if request.method != "POST":
        messages.error(request, "Invalid Method.")
        return redirect('users:student_feedback')
    else:
        feedback = request.POST.get('feedback_message')
        student_obj = user_profile_student.objects.get(user=request.user)

        try:
            add_feedback = FeedBackStudent(student=student_obj, feedback=feedback, feedback_reply="")
            add_feedback.save()
            # messages.success(request, "Feedback Sent.")
            return redirect('users:student_feedback')
        except:
            messages.error(request, "Failed to Send Feedback.")
            return redirect('users:student_feedback')

def notifications(request):
    user=request.user
    student=user_profile_student.objects.get(user=user)
    notifications = NotificationStudent.objects.filter(student_id=student).order_by('-id')
    return render(request, 'student_template/notification.html', {'notifications': notifications})

def mark_notification_as_read(request, id):
    notification = NotificationStudent.objects.get(id=id)
    notification.read = True
    notification.save()
    return redirect('users:student_feedback')

# def unread_notification(request):
#     user=request.user
#     student=user_profile_student.objects.filter(user=user)
#     unread_notifications = NotificationStudent.objects.filter(student_id=student, read=False).count()
#     return render(request, 'student_temp/dashboard.html', {'unread_notifications': unread_notifications})