from django import forms

class AddStudentForm(forms.Form):
    username=forms.CharField(min_length=5, max_length=150,required=True)
    email=forms.EmailField(required=True)
    password1=forms.CharField(widget=forms.PasswordInput())
    password2=forms.CharField(widget=forms.PasswordInput())
    First_Name=forms.CharField(required=True)
    Middle_Name=forms.CharField(required=False)
    Last_Name=forms.CharField(required=True)
    dob=forms.DateField(widget =forms.NumberInput(attrs={'type':'date'}))
    grade=forms.CharField(required=True)
    school=forms.CharField(required=True)
    country=forms.CharField(required=False)
    state=forms.CharField(required=False)
    city=forms.CharField(required=False)