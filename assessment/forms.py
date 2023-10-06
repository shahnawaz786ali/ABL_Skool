from django import forms
from .models import *

class AssessmentForm(forms.ModelForm):
    class Meta:
        model = Assessment
        fields = ['username', 'camera_image']
