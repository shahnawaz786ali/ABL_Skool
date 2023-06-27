from django.contrib import admin
from users.models import *

class studentadmin(admin.ModelAdmin):
    list_display=('first_name', 'school')
    list_filter=('school','grade')

# Register your models here.
admin.site.register(Contact)
admin.site.register(User)
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
admin.site.register(NotificationStudent)
admin.site.register(UserLoginActivity)