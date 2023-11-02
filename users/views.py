from django.shortcuts import render,redirect
from django.http import HttpResponseRedirect
from django.contrib.auth import logout,login
from django.http import HttpResponse
from django.contrib.auth.decorators import login_required
from users.models import Contact,User
from users.forms import studentsignupform,parentsignupform,teachersignupform,principalsignupform,schoolsignupform
from django.views.generic import CreateView,FormView
from django.contrib import messages
from users.Emailbackend import EmailBackEnd
import requests
import json
from users.models import *
from .forms import *
from .utils import activateEmail
import datetime as dt
from curriculum.models import *

def index(request):
    return render(request,"users/index.html")
    # if request.user.is_authenticated:
    #     context={'time':my_view(request)}
    #     return render(request,"users/index.html",context)
    # else:
    #     return render(request,"users/index.html")

# def my_view(request):
#     logout_time=request.session.get('last_logout')
#     login_time=request.session.get('last_login')
#     time_out=dt.datetime.strptime(logout_time, '%Y-%m-%d %H:%M:%S.%f')
#     time_in=dt.datetime.strptime(login_time, '%Y-%m-%d %H:%M:%S.%f')

#     time_out_minute=time_out.minute
#     print(time_out_minute)
#     time_in_minute=time_in.minute
#     print(time_in_minute)
#     absent=time_out_minute-time_in_minute
#     print(absent)
    
def account_activation(request):
    return render(request, "users/account_activation.html")

class StudentSignUpView(FormView):
    model = User
    form_class = studentsignupform
    template_name = 'users/student.html'

    def get_context_data(self,**kwargs):
        kwargs['user_type'] = 'student'
        return super().get_context_data(**kwargs)

    def form_valid(self,form):
        user = form.save()
        to=user.email
        # activateEmail(self.request, user, to) 
        return redirect('users:index')

class ParentSignUpView(CreateView):
    model = User
    form_class = parentsignupform
    template_name = 'users/parent.html'

    def get_context_data(self, **kwargs):
        kwargs['user_type'] = 'parent'
        return super().get_context_data(**kwargs)

    def form_valid(self,form):
        user =form.save()
        to=user.email
        activateEmail(self.request, user, to)       
        return redirect('users:message')

class TeacherSignUpView(CreateView):
    model = User
    form_class = teachersignupform
    template_name = 'users/teacher.html'

    def get_context_data(self, **kwargs):
        kwargs['user_type'] = 'teacher'
        return super().get_context_data(**kwargs)

    def form_valid(self, form):
        user = form.save()
        to=user.email
        activateEmail(self.request, user, to) 
        return redirect('users:index')

class PrincipalSignUpView(CreateView):
    model = User
    form_class = principalsignupform
    template_name = 'users/principal.html'

    def get_context_data(self, **kwargs):
        kwargs['user_type'] = 'principal'
        return super().get_context_data(**kwargs)

    def form_valid(self, form):
        user = form.save()
        to=user.email
        activateEmail(self.request, user, to) 
        return redirect('users:index')

class SchoolSignUpView(CreateView):
    model = User
    form_class = schoolsignupform
    template_name = 'users/school.html'

    def get_context_data(self, **kwargs):
        kwargs['user_type'] = 'school'
        return super().get_context_data(**kwargs)

    def form_valid(self, form):
        user = form.save()
        to=user.email
        # activateEmail(self.request, user, to) 
        return redirect('users:index')
    
def mark_attendance(request):
    user = request.user
    user1=User.objects.get(username=user)
    current_date = date.today()

    attendance = Attendance(user=user1, date=current_date)
    attendance.save()

def user_login(request):
    if request.method == "POST":
        password = request.POST.get('password')
        email=request.POST.get('email')

        # capcha_token=request.POST.get("g-recaptcha-response")
        # cap_url="https://www.google.com/recaptcha/api/siteverify"
        # cap_secret="6LeLgcEkAAAAAPQMUQSoVzHMQwwmCQx_UATRgoaE"
        # cap_data={"secret":cap_secret, "response":capcha_token}
        # cap_server_response=requests.post(url=cap_url, data=cap_data)
        # print(cap_server_response.text)
        # cap_json=json.loads(cap_server_response.text)
        # if cap_json['success']==False:
        #     # messages.error(request,"Invalid Captcha Try Again")
        #     return HttpResponseRedirect("/")

        user =EmailBackEnd.authenticate(request,username=email, password=password)
    
        if user is not None:
            if user.is_active:
                login(request,user)
                return render (request,'users/index.html')
            else:
                return HttpResponse("User not verified!")         
        else:
            return HttpResponse("Please use correct id and password")

    else:
        return render(request, 'users/login.html')

@login_required
def user_logout(request):
    logout(request)
    # messages.success(request,"You have successfully logout")
    return render(request, 'users/index.html')

def register(request):
    return render(request, 'users/register.html')

def contact(request):
    if request.method=="POST":
        name=request.POST.get('name')
        contact_num=request.POST.get('contact')
        email=request.POST.get('email')
        message=request.POST.get('message')

        con=Contact(name=name, contact_no=contact_num, mail=email, message=message)
        con.save()
    return render(request, "users/contact.html")   

def studentreport(request):
    return render(request, "users/student_report.html")

def editor(request):
    return render(request, "users/editor.html")

def editor_index(request):
    return render(request, "users/editor_index.html")


def student_dasboard(request):
    students=User.objects.filter(username=request.user)
    return render(request, "dashboard/index.html",{"students":students})

def enquiry(request):
    if request.method=="POST":
        name=request.POST.get('name')
        contact_num=request.POST.get('contact')
        email=request.POST.get('email')
        enquiry=request.POST.get('query')

        capcha_token=request.POST.get("g-recaptcha-response")
        cap_url="https://www.google.com/recaptcha/api/siteverify"
        cap_secret="6LeLgcEkAAAAAPQMUQSoVzHMQwwmCQx_UATRgoaE"
        cap_data={"secret":cap_secret, "response":capcha_token}
        cap_server_response=requests.post(url=cap_url, data=cap_data)
        print(cap_server_response.text)
        cap_json=json.loads(cap_server_response.text)
        if cap_json['success']==False:
            # messages.error(request,"Invalid Captcha Try Again")
            return HttpResponseRedirect("/")

        enquiry1=Enquiry(name=name, contact=contact_num, email=email, query=enquiry)
        enquiry1.save()

    return HttpResponse("Thank you for your response. We will get back to you.")

def message(request):
    return render(request,"users/message.html")

from .forms import DemoBookingForm
from .models import DemoBooking

def book_demo(request):
    if request.method == 'POST':
        form = DemoBookingForm(request.POST)
        if form.is_valid():
            # Create and save a DemoBooking object with the submitted data
            demo_booking = DemoBooking(
                parent_name=form.cleaned_data['parent_name'],
                parent_mobile=form.cleaned_data['parent_mobile'],
                parent_email=form.cleaned_data['parent_email'],
                student_name=form.cleaned_data['student_name'],
                course=form.cleaned_data['course'],
                slot_date=form.cleaned_data['slot_date']
            )
            demo_booking.save()
            return redirect('users:success_page')

    else:
        form = DemoBookingForm()

    return render(request, 'users/demo.html', {'form': form})

def success_page(request):
    return render(request,'users/demo_success.html')

# import gspread
# from oauth2client.service_account import ServiceAccountCredentials

# # Load the credentials from the JSON file
# scope = ["https://spreadsheets.google.com/feeds", "https://www.googleapis.com/auth/drive"]
# creds = ServiceAccountCredentials.from_json_keyfile_name('C:\\Users\\admin\\Pictures\\abl-lms\\lms\\static\\Images\\credential.json', scope)
# client = gspread.authorize(creds)

# spreadsheet = client.open('Turtle (Responses)')

# # Select the specific worksheet
# worksheet = spreadsheet.worksheet('Turtle_Response')

# # Get all values from the worksheet
# # data = worksheet.get_all_values()
# data = worksheet.col_values(1)

# for row in data:
#     # Parse data from the row, e.g., student name, score, etc.
#     student_name = row[2]
#     print(student_name)
#     score = row[1]

#     user=User.objects.get(username=student_name)

#     student_score=Topicwise_Marks(student=user,marks=score)
#     student_score.save()
    # Create or update the database record
    # student, created = StudentScore.objects.get_or_create(name=student_name)
    # student.score = score
    # student.save()