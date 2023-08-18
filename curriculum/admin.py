from django.contrib import admin
from .models import *
from django_admin_listfilter_dropdown.filters import DropdownFilter, RelatedDropdownFilter, ChoiceDropdownFilter

# Register your models here.
class standardadmin(admin.ModelAdmin):
    list_display=['name',]

class subjectadmin(admin.ModelAdmin):
    list_display=['name','standard',]
    search_fields=('name',)
    list_filter=(('name', DropdownFilter),
        # for choice fields
        # ('grade', ChoiceDropdownFilter),
        # for related fields
        ('standard', RelatedDropdownFilter))

class lessonadmin(admin.ModelAdmin):
    list_display=['name','subject','Standard',]
    list_filter=(('name', DropdownFilter),
        ('Standard', RelatedDropdownFilter),
        ('subject', RelatedDropdownFilter)
        )
    search_fields=('name',)

admin.site.register(Standard,standardadmin)
admin.site.register(Subject,subjectadmin)
admin.site.register(Lesson,lessonadmin)
admin.site.register(AILesson)
admin.site.register(AISubject)
admin.site.register(Comment)
admin.site.register(Reply)
admin.site.register(CodingSubject)
admin.site.register(CodingLesson)
admin.site.register(StudentResult)
admin.site.register(Mechanzo)
admin.site.register(Mechanzo_kit_name)
admin.site.register(Mechanzo_model_name)
admin.site.register(Topicwise_Marks)