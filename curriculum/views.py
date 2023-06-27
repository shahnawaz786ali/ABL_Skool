from django.shortcuts import render,HttpResponseRedirect,redirect
from django.views.generic import ListView,DetailView,CreateView,UpdateView,DeleteView,FormView,TemplateView
from .models import Standard,Subject,Lesson,AISubject,AILesson,CodingSubject,CodingLesson,Comment
from django.urls import reverse_lazy
from .forms import CommentForm,ReplyForm, LessonForm
from rest_framework import viewsets
from .serializers import standardserializer,SubjectSerializer
from django.db.models import Q
from django.core.paginator import Paginator
from django.contrib.auth import get_user_model
from django.conf import settings
from django.views.decorators.cache import cache_page
from django.core.cache.backends.base import DEFAULT_TIMEOUT
from django.core.cache import cache
from django.utils.decorators import method_decorator

CACHE_TTL = getattr(settings ,'CACHE_TTL' , DEFAULT_TIMEOUT)

# Create your views here.
class StandardListView(ListView):
    context_object_name = 'standards'
    model = Standard
    template_name = 'curriculum/standard_list_view.html'

# @method_decorator(cache_page(60 * 60*24), name='dispatch')
class SubjectListView(DetailView):
    context_object_name = 'standards'
    model = Standard
    template_name = 'curriculum/subject_list_view.html'

    # def get_context_data(self,**kwargs):
    #     context = super().get_context_data(**kwargs)
    #     num_visits = self.request.session.get('num_visits', 0)
    #     self.request.session['num_visits'] = num_visits + 1
    #     context['num_visits']=num_visits
    #     print(num_visits)
    #     return context

# @method_decorator(cache_page(60*60*24), name='dispatch')
class LessonListView(DetailView):
    context_object_name = 'subjects'
    model = Subject
    template_name = 'curriculum/lesson_list_view.html'

# @method_decorator(cache_page(60*60*24), name='dispatch')
class LessonDetailView(DetailView,FormView):
    context_object_name = 'lessons'
    model = Lesson
    template_name = 'curriculum/lesson_detail_view.html'
    form_class = CommentForm
    second_form_class = ReplyForm

    def get_context_data(self, **kwargs):
        context = super(LessonDetailView, self).get_context_data(**kwargs)
        if 'form' not in context:
            context['form'] = self.form_class(request=self.request)
        if 'form2' not in context:
            context['form2'] = self.second_form_class(request=self.request)
        # context['comments'] = Comment.objects.filter(id=self.object.id)
        return context
    
    def post(self, request, *args, **kwargs):
        self.object = self.get_object()
        if 'form' in request.POST:
            form_class = self.get_form_class()
            form_name = 'form'
        else:
            form_class = self.second_form_class
            form_name = 'form2'

        form = self.get_form(form_class)

        if form_name=='form' and form.is_valid():
            print("comment form is returned")
            return self.form_valid(form)
        elif form_name=='form2' and form.is_valid():
            print("reply form is returned")
            return self.form2_valid(form)

    def get_success_url(self):
        self.object = self.get_object()
        standard = self.object.Standard
        subject = self.object.subject
        return reverse_lazy('curriculum:lesson_detail',kwargs={'standard':standard.slug, 'subject':subject.slug,'slug':self.object.slug})
    
    def form_valid(self, form):
        self.object = self.get_object()
        fm = form.save(commit=False)
        fm.author = self.request.user
        fm.lesson_name = self.object.comments.name
        fm.lesson_name_id = self.object.id
        fm.save()
        return HttpResponseRedirect(self.get_success_url())

    def form2_valid(self, form):
        self.object = self.get_object()
        fm = form.save(commit=False)
        fm.author = self.request.user
        fm.comment_name_id = self.request.POST.get('comment.id')
        fm.save()
        return HttpResponseRedirect(self.get_success_url())


class LessonCreateView(CreateView):
    # fields = ('lesson_id','name','position','image','video','ppt','Notes')
    form_class = LessonForm
    context_object_name = 'subject'
    model= Subject
    template_name = 'curriculum/lesson_create.html'

    def get_success_url(self):
        self.object = self.get_object()
        standard = self.object.standard
        return reverse_lazy('curriculum:lesson_list',kwargs={'standard':standard.slug,
                                                             'slug':self.object.slug})


    def form_valid(self, form, *args, **kwargs):
        self.object = self.get_object()
        fm = form.save(commit=False)
        fm.created_by = self.request.user
        fm.Standard = self.object.standard
        fm.subject = self.object
        fm.save()
        return HttpResponseRedirect(self.get_success_url())

class LessonUpdateView(UpdateView):
    fields = ('name','position','video','ppt','Notes')
    model= Lesson
    template_name = 'curriculum/lesson_update.html'
    context_object_name = 'lessons'

class LessonDeleteView(DeleteView):
    model= Lesson
    context_object_name = 'lessons'
    template_name = 'curriculum/lesson_delete.html'

    def get_success_url(self):
        print(self.object)
        standard = self.object.Standard
        subject = self.object.subject
        return reverse_lazy('curriculum:lesson_list',kwargs={'standard':standard.slug,'slug':subject.slug})
    
def ai(request):
    subjects=AISubject.objects.all()
    return render(request, "ai/ai.html",{"subjects":subjects})

def lessons(request,slug):
    subjects=AISubject.objects.get(slug=slug)
    lessons=AILesson.objects.filter(subject=subjects)
    return render(request, "ai/lessons.html", {"subjects":subjects, "lessons":lessons})

def lesson_detail(request,slug):
    subjects=AISubject.objects.all()
    lessons=AILesson.objects.get(slug=slug)
    return render(request, "ai/lesson_detail.html", {"subjects":subjects, "lessons":lessons})

def coding(request):
    return render(request, "coding/coding.html")

def codinglessons(request,slug):
    subjects=CodingSubject.objects.get(slug=slug)
    lessons=CodingLesson.objects.filter(subject=subjects)
    return render(request, "coding/codinglessons.html", {"subjects":subjects, "lessons":lessons})

def codinglesson_detail(request,slug):
    subjects=CodingSubject.objects.all()
    lessons=CodingLesson.objects.get(slug=slug)
    return render(request, "coding/codinglesson_detail.html", {"subjects":subjects, "lessons":lessons})

def training_level(request):
    return render(request, "trainer/training_level.html")

def trainer_subject_1(request):
    subjects=Subject.objects.filter(Q(subject_id='scratch_5') | Q(subject_id='mit') | Q(subject_id='js') | Q(subject_id='python'))
    return render(request, "trainer/subject.html",{"subjects":subjects})

def trainer_subject_2(request):
    subjects=Subject.objects.filter(Q(subject_id='arduino_uno_8') | Q(subject_id='python_8') | Q(subject_id="robotics"))
    return render(request, "trainer/subject.html",{"subjects":subjects})

def trainer_subject_3(request):
    subjects=Subject.objects.filter(Q(subject_id='python_9') | Q(subject_id='ai_11'))
    return render(request, "trainer/subject.html",{"subjects":subjects})

def trainer_lesson(request,slug):
    subjects=Subject.objects.get(slug=slug)
    lessons=Lesson.objects.filter(subject=subjects)
    if subjects.slug=="python":
        lessons=lessons.filter(Q(lesson_id="python_7_1") | Q(lesson_id="python_7_2"))

    elif subjects.slug=="arduino_uno_8":
        lessons=lessons.filter(Q(lesson_id="arduino_7_1"))
    return render(request, "trainer/trainer_lesson.html", {"subjects":subjects, "lessons":lessons})


def trainer_lesson_detail(request,slug):
    subjects=Subject.objects.all()
    lessons=Lesson.objects.get(slug=slug)
    return render(request,"trainer/trainer_lesson_detail.html",{"subject":subjects,"lessons":lessons})
