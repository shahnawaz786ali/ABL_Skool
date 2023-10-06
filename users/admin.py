from django.contrib import admin
from users.models import *

class studentadmin(admin.ModelAdmin):
    list_display=('first_name', 'school')
    list_filter=('school','grade')

class useradmin(admin.ModelAdmin):
    search_fields=('username',)

# Register your models here.
admin.site.register(Contact)
admin.site.register(User,useradmin)
admin.site.register(user_profile_teacher)
admin.site.register(user_profile_student,studentadmin)
admin.site.register(user_profile_principal)
admin.site.register(user_profile_school)
admin.site.register(user_profile_parent)
admin.site.register(Enquiry)
admin.site.register(SessionYearModel)
admin.site.register(Attendance)
admin.site.register(AttendanceReport)
admin.site.register(FeedBackStudent)
admin.site.register(FeedBackSchool)
admin.site.register(NotificationStudent)
admin.site.register(NotificationSchool)
admin.site.register(UserLoginActivity)