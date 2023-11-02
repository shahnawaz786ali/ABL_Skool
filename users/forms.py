from django import forms
from django.contrib.auth.forms import UserCreationForm
from users.models import user_profile_student,user_profile_parent,user_profile_principal,user_profile_school,user_profile_teacher,User
from django.core.exceptions import ValidationError

class studentsignupform(UserCreationForm):
    choices=[('Vivekanand School','Vivekanand School'),
             ('New Era Public School','New Era Public School'),
             ('TDI Internation','TDI International'),
             ('Moga Devi School','Moga Devi School')]
    
    choices_grade=[('1','1'),('2','2'),('3','3'),('4','4'),('5','5'),
             ('6','6'),('7','7'),('8','8'),('9','9'),('10','10'),
             ('11','11'),('12','12')]
    username=forms.CharField(min_length=5, max_length=150,required=True,label="Username")
    email=forms.EmailField(required=True,label="Email")
    password1=forms.CharField(widget=forms.PasswordInput,label="Password")
    password2=forms.CharField(widget=forms.PasswordInput(),label="Confirm Password")
    First_Name=forms.CharField(required=True,label="First Name")
    Middle_Name=forms.CharField(required=False,label="Middle Name")
    Last_Name=forms.CharField(required=True,label="Last Name")
    dob=forms.DateField(widget =forms.NumberInput(attrs={'type':'date'}),label="DOB")
    grade=forms.CharField(required=True,label="Grade",widget=forms.Select(attrs={'class': 'form-control'},choices=choices_grade))
    school=forms.CharField(required=True,label="School",widget=forms.Select(attrs={'class': 'form-control'},choices=choices))
    country=forms.CharField(required=False,label="Country")
    state=forms.CharField(required=False,label="State")
    city=forms.CharField(required=False,label="City")
    # profile_pic = forms.FileField(label="Profile Pic", required=False, widget=forms.FileInput(attrs={"class":"form-control"}))

    class Meta(UserCreationForm.Meta):
        model=User

    def username_clean(self):  
        username = self.cleaned_data['username'].lower()  
        new = user_profile_student.objects.filter(username = username)  
        if new.count():  
            raise ValidationError("User Already Exist")
        return username  

    def clean_email(self):
        email = self.cleaned_data['email']
        if User.objects.filter(email=email).exists():
            raise ValidationError("Email already exists")
        return email  
  
    def clean_password2(self):  
        password1 = self.cleaned_data['password1']  
        password2 = self.cleaned_data['password2']  
  
        if password1 and password2 and password1 != password2:  
            raise ValidationError("Password don't match")  
        return password2 
        
    def __init__(self, *args, **kwargs):
        super(studentsignupform, self).__init__(*args, **kwargs)
        self.fields['password1'].help_text = None
        self.fields['password2'].help_text = None
        self.fields['username'].help_text = None
        self.label_suffix = ""

    def save(self):
        user = super().save(commit=False)
        user.email=self.cleaned_data.get('email')
        user.is_student = True
        user.is_active=False
        user.save()
        student = user_profile_student.objects.create(user=user)
        student.username=self.cleaned_data.get('username')
        student.password1=self.cleaned_data.get('password1')
        student.first_name=self.cleaned_data.get('First_Name')
        student.middle_name=self.cleaned_data.get('Middle_Name')
        student.last_name=self.cleaned_data.get('Last_Name')
        student.grade=self.cleaned_data.get('grade')
        student.school=self.cleaned_data.get('school')
        student.country=self.cleaned_data.get('country')
        student.state=self.cleaned_data.get('state')
        student.city=self.cleaned_data.get('city')
        student.profile_pic=self.cleaned_data.get('profile_pic')
        student.save()
        return user

class parentsignupform(UserCreationForm):  
    username = forms.CharField(min_length=5, max_length=150,label="Username")  
    email = forms.EmailField(label="Email")  
    password1 = forms.CharField(widget=forms.PasswordInput,label="Password")  
    password2 = forms.CharField(widget=forms.PasswordInput,label="Confirm Password")
    First_Name=forms.CharField(required=True,label="First Name")
    Middle_Name=forms.CharField(required=False,label="Middle Name")
    Last_Name=forms.CharField(required=True,label="Last Name")
    Mobile=forms.CharField(required=True,label="Mobile Number")

    class Meta(UserCreationForm.Meta):
        model=User

  
    def username_clean(self):  
        username = self.cleaned_data['username'].lower()  
        new = user_profile_parent.objects.filter(username = username)  
        if new.count():  
            raise ValidationError("User Already Exist")  
        return username  
  
    def clean_email(self):
        email = self.cleaned_data['email']
        if User.objects.filter(email=email).exists():
            raise ValidationError("Email already exists")
        return email 
  
    def clean_password2(self):  
        password1 = self.cleaned_data['password1']  
        password2 = self.cleaned_data['password2']  
  
        if password1 and password2 and password1 != password2:  
            raise ValidationError("Password don't match")  
        return password2  
        
    def __init__(self, *args, **kwargs):
        super(parentsignupform, self).__init__(*args, **kwargs)
        self.fields['password1'].help_text = None
        self.fields['password2'].help_text = None
        self.fields['username'].help_text = None
        self.label_suffix = ""
  
    def save(self):  
        user = super().save(commit=False)
        user.email=self.cleaned_data.get('email')
        user.otp=self.cleaned_data.get('otp')
        user.is_parent = True
        user.is_active=False
        user.save()
        parent= user_profile_parent.objects.create(user=user) 
        parent.username=self.cleaned_data['username']  
        parent.password1=self.cleaned_data['password1']
        parent.first_name=self.cleaned_data['First_Name']
        parent.middle_name=self.cleaned_data['Middle_Name']
        parent.last_name=self.cleaned_data['Last_Name']
        parent.mobile=self.cleaned_data['Mobile']
        parent.save()
        return user 
        
class teachersignupform(UserCreationForm): 
    choices=[('Vivekanand School','Vivekanand School'),
             ('New Era Public School','New Era Public School'),
             ('TDI Internation','TDI International'),
             ('Moga Devi School','Moga Devi School')]
     
    username = forms.CharField(min_length=5, max_length=150,label="Username")  
    email = forms.EmailField(label="Email")  
    password1 = forms.CharField(widget=forms.PasswordInput,label="Password")  
    password2 = forms.CharField(widget=forms.PasswordInput,label="Confirm Password")
    First_Name=forms.CharField(required=True,label="First Name")
    Middle_Name=forms.CharField(required=False,label="Middle Name")
    Last_Name=forms.CharField(required=True,label="Last Name")
    Mobile=forms.CharField(required=True,label="Mobile Number")
    grade=forms.CharField(required=False,label="Grade")
    school=forms.CharField(required=True,label="School",widget=forms.Select(choices=choices))

    class Meta(UserCreationForm.Meta):
        model=User
  
    def username_clean(self):  
        username = self.cleaned_data['username'].lower()  
        new = user_profile_teacher.objects.filter(username = username)  
        if new.count():  
            raise ValidationError("User Already Exist")  
        return username  
  
    def clean_email(self):
        email = self.cleaned_data['email']
        if User.objects.filter(email=email).exists():
            raise ValidationError("Email already exists")
        return email 
  
    def clean_password2(self):  
        password1 = self.cleaned_data['password1']  
        password2 = self.cleaned_data['password2']  
  
        if password1 and password2 and password1 != password2:  
            raise ValidationError("Password don't match")  
        return password2  
    
    def __init__(self, *args, **kwargs):
        super(teachersignupform, self).__init__(*args, **kwargs)
        self.fields['password1'].help_text = None
        self.fields['password2'].help_text = None
        self.fields['username'].help_text = None
        self.label_suffix = ""
  
    def save(self):  
        user = super().save(commit=False)
        user.email=self.cleaned_data.get('email')
        user.is_teacher = True
        user.is_active=False
        user.save()
        teacher= user_profile_teacher.objects.create(user=user) 
        teacher.username=self.cleaned_data['username']  
        teacher.password1=self.cleaned_data['password1'] 
        teacher.first_name=self.cleaned_data['First_Name']
        teacher.middle_name=self.cleaned_data['Middle_Name']
        teacher.last_name=self.cleaned_data['Last_Name']
        teacher.mobile=self.cleaned_data['Mobile']
        teacher.grade=self.cleaned_data['grade']
        teacher.school=self.cleaned_data['school']
        teacher.save()
        return user


class principalsignupform(UserCreationForm):  
    username = forms.CharField(min_length=5, max_length=150,label="Username")  
    email = forms.EmailField(label="Email")  
    password1 = forms.CharField(widget=forms.PasswordInput,label="Password")  
    password2 = forms.CharField(widget=forms.PasswordInput,label="Confirm Password")
    First_Name=forms.CharField(required=True,label="First Name")
    Middle_Name=forms.CharField(required=False,label="Middle Name")
    Last_Name=forms.CharField(required=True,label="Last Name")
    Mobile=forms.CharField(required=True,label="Mobile Number")
    school=forms.CharField(required=True,label="School")

    class Meta(UserCreationForm.Meta):
        model=User
  
    def username_clean(self):  
        username = self.cleaned_data['username'].lower()  
        new = user_profile_principal.objects.filter(username = username)  
        if new.count():  
            raise ValidationError("User Already Exist")  
        return username  
  
    def clean_email(self):
        email = self.cleaned_data['email']
        if User.objects.filter(email=email).exists():
            raise ValidationError("Email already exists")
        return email 
  
    def clean_password2(self):  
        password1 = self.cleaned_data['password1']  
        password2 = self.cleaned_data['password2']  
  
        if password1 and password2 and password1 != password2:  
            raise ValidationError("Password don't match")  
        return password2  
    
    def __init__(self, *args, **kwargs):
        super(principalsignupform, self).__init__(*args, **kwargs)
        self.fields['password1'].help_text = None
        self.fields['password2'].help_text = None
        self.fields['username'].help_text = None
        self.label_suffix = ""
  
    def save(self):  
        user = super().save(commit=False)
        user.email=self.cleaned_data.get('email')
        user.is_principal = True
        user.is_active=False
        user.save()
        principal= user_profile_principal.objects.create(user=user) 
        principal.username=self.cleaned_data['username']  
        principal.password1=self.cleaned_data['password1'] 
        principal.first_name=self.cleaned_data['First_Name']
        principal.middle_name=self.cleaned_data['Middle_Name']
        principal.last_name=self.cleaned_data['Last_Name']
        principal.mobile=self.cleaned_data['Mobile']
        principal.school=self.cleaned_data['school']
        principal.save()
        return user

class schoolsignupform(UserCreationForm):
    username=forms.CharField(min_length=5, max_length=150,required=True,label="Username")
    email=forms.EmailField(required=True,label="Email")
    password1=forms.CharField(widget=forms.PasswordInput(),label="Password")
    password2=forms.CharField(widget=forms.PasswordInput(),label="Confirm Password")
    School_Name=forms.CharField(required=True,label="School Name")
    phone=forms.CharField(required=True,label="Phone Number")
    mobile=forms.CharField(required=True,label="Mobile Number")
    established=forms.DateField(widget =forms.NumberInput(attrs={'type':'date'}),label="Year of Establishment")
    country=forms.CharField(required=False,label="Country")
    state=forms.CharField(required=False,label="State")
    city=forms.CharField(required=False,label="City")
    pin=forms.CharField(required=True,label="Pincode")

    class Meta(UserCreationForm.Meta):
        model=User

    def username_clean(self):  
        username = self.cleaned_data['username'].lower()  
        new = user_profile_school.objects.filter(username = username)  
        if new.count():  
            raise ValidationError("User Already Exist")  
        return username  
  
    def email_clean(self):  
        email = self.cleaned_data['email'].lower()  
        new = user_profile_school.objects.filter(email=email)  
        if new.count():  
            raise ValidationError(" Email Already Exist")  
        return email  
  
    def clean_password2(self):  
        password1 = self.cleaned_data['password1']  
        password2 = self.cleaned_data['password2']  
  
        if password1 and password2 and password1 != password2:  
            raise ValidationError("Password don't match")  
        return password2 
    
    def __init__(self, *args, **kwargs):
        super(schoolsignupform, self).__init__(*args, **kwargs)
        self.fields['password1'].help_text = None
        self.fields['password2'].help_text = None
        self.fields['username'].help_text = None
        self.label_suffix = ""

    def save(self):
        user = super().save(commit=False)
        user.email=self.cleaned_data.get('email')
        user.is_school= True
        user.is_active=False
        user.save()
        school = user_profile_school.objects.create(user=user)
        school.username=self.cleaned_data.get('username')
        school.password1=self.cleaned_data.get('password1')
        school.school_name=self.cleaned_data.get('School_Name')
        school.phone=self.cleaned_data.get('phone')
        school.mobile=self.cleaned_data.get('mobile')
        school.country=self.cleaned_data.get('country')
        school.state=self.cleaned_data.get('state')
        school.city=self.cleaned_data.get('city')
        school.pin=self.cleaned_data.get('pin')
        school.district=self.cleaned_data.get('district')
        school.principal=self.cleaned_data.get('principal')
        school.mentor=self.cleaned_data.get('mentor')
        school.logo=self.cleaned_data.get('logo')
        school.save()
        return user

class DemoBookingForm(forms.Form):
    parent_name = forms.CharField(max_length=100, label="Parent's Name")
    parent_mobile = forms.CharField(max_length=15, label="Parent's Mobile Number")
    parent_email = forms.EmailField(label="Parent's Email")
    student_name = forms.CharField(max_length=100, label="Student's Name")
    course = forms.CharField(max_length=100, label="Course")
    slot_date = forms.DateField(widget=forms.DateInput(attrs={'type': 'date'}), label="Preferred Date")
    slot_time = forms.ChoiceField(choices=[('morning', 'Morning'), ('evening', 'Evening')])