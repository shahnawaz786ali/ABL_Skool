from django.shortcuts import render,HttpResponseRedirect,HttpResponse
from users.models import *
from curriculum.models import *
from .forms import AddStudentForm
from django.contrib import messages

# Create your views here.
def signup_admin(request):
    return render(request, "admin-temp/base_template.html")

def admin_home(request):
    student=user_profile_student.objects.all().count()
    parent=user_profile_parent.objects.all().count()
    teacher=user_profile_teacher.objects.all().count()
    principal=user_profile_principal.objects.all().count()
    school=user_profile_school.objects.all().count()

    subjects=Subject.objects.all().count()
    lessons=Lesson.objects.all().count()
    grades=Standard.objects.all().count()

    return render(request, "admin-temp/home_content.html", {"student":student, "parent":parent, "teacher":teacher, "principal":principal, "school":school, "subjects":subjects, "lessons":lessons,"grades":grades})

def add_grade(request):
    return render(request,"admin-temp/add_class.html")

def add_grade_save(request):
    if request.method!="POST":
        return HttpResponse("Method Not Allowed")
    else:
        grade=request.POST.get("grade")
        desc=request.POST.get("desc")
        try:
            grade=Standard(name=grade)
            grade.description=desc
            grade.save()
            messages.success(request,"Successfully Added Course")
            return HttpResponseRedirect(reverse("customadmin:add_grade"))
        except Exception as e:
            print(e)
            messages.error(request,"Failed To Add Course")
            return HttpResponseRedirect(reverse("customadmin:add_grade"))
        
def manage_grade(request):
    grades=Standard.objects.all()
    return render(request,'admin-temp/manage_grade.html', {'grades':grades})

def edit_grade(request,grade_id):
    grades=Standard.objects.get(id=grade_id)
    return render(request,"admin-temp/edit_grade.html",{"grades":grades,"id":grade_id})

def edit_grade_save(request):
    if request.method!="POST":
        return HttpResponse("<h2>Method Not Allowed</h2>")
    else:
        grade_id=request.POST.get("grade_id")
        grade_name=request.POST.get("grade_name")
        desc=request.POST.get("desc")

        try:
            grade=Standard.objects.get(id=grade_id)
            grade.name=grade_name
            grade.description=desc
            grade.save()

            messages.success(request,"Successfully Edited grade")
            return HttpResponseRedirect(reverse("customadmin:edit_grade",kwargs={"grade_id":grade_id}))
        except:
            messages.error(request,"Failed to Edit grade")
            return HttpResponseRedirect(reverse("customadmin:edit_grade",kwargs={"grade_id":grade_id}))

def add_subject(request):
    grades=Standard.objects.all()
    return render(request,"admin-temp/add_subject_template.html",{"grades":grades})

def add_subject_save(request):
    if request.method!="POST":
        return HttpResponse("<h2>Method Not Allowed</h2>")
    else:
        subject_id=request.POST.get("subject_id")
        subject_name=request.POST.get("subject_name")
        grade_id=request.POST.get('grade')
        grade=Standard.objects.get(pk=grade_id)
        image=request.POST.get('filename')
        desc=request.POST.get("description")

        try:
            subject=Subject(subject_id=subject_id,name=subject_name,description=desc,standard=grade,image=image)
            subject.save()
            messages.success(request,"Successfully Added Subject")
            return HttpResponseRedirect(reverse("customadmin:add_subject"))
        except:
            messages.error(request,"Failed to Add Subject")
            return HttpResponseRedirect(reverse("customadmin:add_subject"))
        
def manage_subject(request):
    subjects=Subject.objects.all()
    return render(request,"admin-temp/manage_subject_template.html",{"subjects":subjects})

def edit_subject(request,subject_id):
    subjects=Subject.objects.get(subject_id=subject_id)
    grades=Standard.objects.all()
    return render(request,"admin-temp/edit_subject_template.html",{"subjects":subjects,"grades":grades,"id":subject_id})

def edit_subject_save(request):
    if request.method!="POST":
        return HttpResponse("<h2>Method Not Allowed</h2>")
    else:
        subject_id=request.POST.get("subject_id")
        subject_name=request.POST.get("subject_name")
        grade_id=request.POST.get('grade')
        grade=Standard.objects.get(pk=grade_id)
        image=request.POST.get('filename')
        desc=request.POST.get("description")

        try:
            subject=Subject.objects.get(subject_id=subject_id)
            subject.name=subject_name
            subject.standard=grade
            subject.image=image
            subject.description=desc
            subject.save()

            messages.success(request,"Successfully Edited Subject")
            return HttpResponseRedirect(reverse("customadmin:edit_subject",kwargs={"subject_id":subject_id}))
        except:
            messages.error(request,"Failed to Edit Subject")
            return HttpResponseRedirect(reverse("customadmin:edit_subject",kwargs={"subject_id":subject_id}))
        
def add_lesson(request):
    grades=Standard.objects.all()
    subjects=Subject.objects.all()
    users=User.objects.filter(is_superuser=True)
    return render(request,"admin-temp/add_lesson.html",{"grades":grades,"subjects":subjects,"users":users})

def add_lesson_save(request):
    if request.method!="POST":
        return HttpResponse("<h2>Method Not Allowed</h2>")
    else:
        lesson_id=request.POST.get("lesson_id")
        grade_id=request.POST.get('grade')
        grade=Standard.objects.get(pk=grade_id)
        user_name=request.POST.get('user')
        created_by=User.objects.get(username=user_name)
        subject_id=request.POST.get('subject')
        subject=Subject.objects.get(id=subject_id)
        name=request.POST.get('lesson_name')
        chapter=request.POST.get('chapter_number')
        video=request.POST.get("video")

        try:
            lessons=Lesson(lesson_id=lesson_id,Standard=grade,created_by=created_by,subject=subject,name=name,position=chapter,video=video)
            lessons.save()
            messages.success(request,"Successfully Added Lesson")
            return HttpResponseRedirect(reverse("customadmin:add_subject"))
        except:
            messages.error(request,"Failed to Add Lesson")
            return HttpResponseRedirect(reverse("customadmin:add_subject"))
        
def manage_lesson(request):
    lesson=Lesson.objects.all()
    return render(request,'admin-temp/manage_lesson.html',{'lesson':lesson})

def edit_lesson(request,lesson_id):
    lessons=Lesson.objects.get(lesson_id=lesson_id)
    subjects=Subject.objects.all()
    grades=Standard.objects.all()
    users=User.objects.filter(is_superuser=True)
    return render(request,"admin-temp/edit_lesson.html",{"lessons":lessons,"subjects":subjects,"grades":grades,"users":users,"id":lesson_id})

def edit_lesson_save(request):
    if request.method!="POST":
        return HttpResponse("<h2>Method Not Allowed</h2>")
    else:
        lesson_id=request.POST.get("lesson_id")
        grade_id=request.POST.get('grade')
        grade=Standard.objects.get(pk=grade_id)
        user_name=request.POST.get('user')
        created_by=User.objects.get(username=user_name)
        subject_id=request.POST.get('subject')
        subject=Subject.objects.get(id=subject_id)
        name=request.POST.get('lesson_name')
        chapter=request.POST.get('chapter_number')
        video=request.POST.get("video")

        try:
            lesson=Lesson.objects.get(lesson_id=lesson_id)
            lesson.name=name
            lesson.Standard=grade
            lesson.created_by=created_by
            lesson.lesson_id=lesson_id
            lesson.position=chapter
            lesson.video=video
            lesson.subject=subject

            messages.success(request,"Successfully Edited Lesson")
            return HttpResponseRedirect(reverse("customadmin:edit_lesson",kwargs={"lesson_id":lesson_id}))
        except:
            messages.error(request,"Failed to Edit Lesson")
            return HttpResponseRedirect(reverse("customadmin:edit_lesson",kwargs={"lesson_id":lesson_id}))
        
def add_student(request):
    form=AddStudentForm()
    return render(request,"admin-temp/add_student_template.html",{"form":form})

def add_student_save(request):
    if request.method!="POST":
        return HttpResponse("Method Not Allowed")
    else:
        form=AddStudentForm(request.POST,request.FILES)
        if form.is_valid():
            username=request.POST.get('username')
            email=request.POST.get('email')
            password1=request.POST.get('password1')
            first_name=request.POST.get('First_Name')
            middle_name=request.POST.get('Middle_Name')
            last_name=request.POST.get('Last_Name')
            dob=request.POST.get('dob')
            grade=request.POST.get('grade')
            school=request.POST.get('school')
            country=request.POST.get('country')
            state=request.POST.get('state')
            city=request.POST.get('city')

            try:
                user=User.objects.create_user(username=username,password=password1,email=email,last_name=last_name,first_name=first_name)          
                user.save()
                messages.success(request,"Successfully Added Student")
                return HttpResponseRedirect(reverse("customadmin:add_student"))
            except:
                messages.error(request,"Failed to Add Student")
                return HttpResponseRedirect(reverse("customadmin:add_student"))
        else:
            form=AddStudentForm(request.POST)
            return render(request, "admin-temp/add_student_template.html", {"form": form})