from django.db import models
from django.contrib.auth.models import AbstractUser
from lms.settings import *
from datetime import date
from django.template.defaultfilters import slugify
import os

# Create your models here.
class User(AbstractUser):
    is_student= models.BooleanField(default=False)
    is_parent= models.BooleanField(default=False)
    is_teacher= models.BooleanField(default=False)
    is_principal= models.BooleanField(default=False)
    is_school= models.BooleanField(default=False)
    is_verified=models.BooleanField(default=False)

def save_profile_image(instance, filename):
    upload_to = 'Images/'
    ext = filename.split('.')[-1]
    # get filename
    if instance.user:
        filename = 'Profile_Pictures/{}.{}'.format(instance.user, ext)
    return os.path.join(upload_to, filename)

class user_profile_student(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, primary_key=True,default="")
    first_name=models.CharField(max_length=50)
    middle_name=models.CharField(max_length=50)
    last_name=models.CharField(max_length=50)
    grade=models.CharField(max_length=50)
    school=models.CharField(max_length=200,default="")
    country=models.CharField(max_length=100)
    state=models.CharField(max_length=50)
    city=models.CharField(max_length=50)
    profile_pic=models.ImageField(upload_to=save_profile_image, blank=True, verbose_name='Profile Image')
    marks_obtained=models.IntegerField(default=0)

    def __str__(self):
        return self.user.username


class user_profile_parent(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, primary_key=True,default="")
    first_name=models.CharField(max_length=50)
    middle_name=models.CharField(max_length=50)
    last_name=models.CharField(max_length=50)
    mobile=models.CharField(max_length=15)

    def __str__(self):
        return self.user.username

class user_profile_teacher(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, primary_key=True,default="")
    first_name=models.CharField(max_length=50)
    middle_name=models.CharField(max_length=50)
    last_name=models.CharField(max_length=50)
    mobile=models.CharField(max_length=15)
    grade=models.IntegerField(null=True)
    school=models.CharField(max_length=200,default="")

    def __str__(self):
        return self.user.username

class user_profile_principal(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, primary_key=True,default="")
    first_name=models.CharField(max_length=50)
    middle_name=models.CharField(max_length=50)
    last_name=models.CharField(max_length=50)
    mobile=models.CharField(max_length=15)
    school=models.CharField(max_length=200,default="")

    def __str__(self):
        return self.user.username

class user_profile_school(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, primary_key=True,default="")
    school_name=models.CharField(max_length=50,default="")
    phone=models.CharField(max_length=50,default="")
    mobile=models.CharField(max_length=15,default="")
    country=models.CharField(max_length=100,default="")
    state=models.CharField(max_length=50,default="")
    city=models.CharField(max_length=50,default="")
    street=models.CharField(max_length=100,default="")
    pin=models.CharField(max_length=50,default="")
    principal=models.CharField(max_length=100,default="")
    mentor=models.CharField(max_length=100,default="")
    district=models.CharField(max_length=100,default="")
    logo=models.ImageField(upload_to="logo/",default="")

    def __str__(self):
        return self.user.username

class Contact(models.Model):
    name=models.CharField(max_length=50)
    contact_no=models.CharField(max_length=15)
    mail=models.EmailField(max_length=50)
    message=models.CharField(max_length=500)

    def __str__(self):
        return self.name
    
class Enquiry(models.Model):
    name=models.CharField(max_length=50)
    contact=models.CharField(max_length=50)
    email=models.EmailField(max_length=50)
    query=models.TextField()

    def __str__(self):
        return self.name

class SessionYearModel(models.Model):
    id = models.AutoField(primary_key=True)
    session_start_year = models.DateField()
    session_end_year = models.DateField()

class Attendance(models.Model):
    user=models.ForeignKey(User, on_delete=models.CASCADE)
    date=models.DateTimeField()

class AttendanceReport(models.Model):
    user= models.ForeignKey(user_profile_student, on_delete=models.DO_NOTHING)
    attendance_id = models.ForeignKey(Attendance, on_delete=models.CASCADE)
    status = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

class FeedBackStudent(models.Model):
    id = models.AutoField(primary_key=True)
    student= models.ForeignKey(user_profile_student, on_delete=models.CASCADE)
    feedback = models.TextField()
    feedback_reply = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.student.first_name

class NotificationStudent(models.Model):
    id = models.AutoField(primary_key=True)
    student_id = models.ForeignKey(user_profile_student, on_delete=models.CASCADE)
    message = models.TextField()
    link = models.URLField(blank=True, null=True)
    read = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.student_id.first_name

class UserLoginActivity(models.Model):
    # Login Status
    SUCCESS = 'S'
    FAILED = 'F'

    LOGIN_STATUS = ((SUCCESS, 'Success'),
                           (FAILED, 'Failed'))

    login_IP = models.GenericIPAddressField(null=True, blank=True)
    login_datetime = models.DateTimeField()
    login_username = models.CharField(max_length=40, null=True, blank=True)
    status = models.CharField(max_length=1, default=SUCCESS, choices=LOGIN_STATUS, null=True, blank=True)
    user_agent_info = models.CharField(max_length=255)
    login_num=models.CharField(max_length=1000,default=0)

    class Meta:
        verbose_name = 'user_login_activity'
        verbose_name_plural = 'user_login_activities'

    def __str__(self):
        return self.login_username
    
class FeedBackSchool(models.Model):
    id = models.AutoField(primary_key=True)
    school= models.ForeignKey(user_profile_school, on_delete=models.CASCADE)
    feedback = models.TextField()
    feedback_reply = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.school.school_name
    
class NotificationSchool(models.Model):
    id = models.AutoField(primary_key=True)
    school_id = models.ForeignKey(user_profile_school, on_delete=models.CASCADE)
    message = models.TextField()
    link = models.URLField(blank=True, null=True)
    read = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.school_id.school_name

class DemoBooking(models.Model):
    parent_name = models.CharField(max_length=100)
    parent_mobile = models.CharField(max_length=15)
    parent_email = models.EmailField()
    student_name = models.CharField(max_length=100)
    course = models.CharField(max_length=100)
    slot_date = models.DateField()
    slot_time = models.TimeField()