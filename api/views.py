from rest_framework import viewsets
from .serializers import standardserializer,SubjectSerializer,LessonSerializer,UserSerializer
from curriculum.models import Standard,Subject,Lesson
from users.models import User
from rest_framework.permissions import IsAuthenticated, IsAdminUser

# Create your views here.
class UserViewSet(viewsets.ModelViewSet):
    queryset=User.objects.all()
    serializer_class=UserSerializer
    permission_classes = (IsAuthenticated,)

class StandardViewSet(viewsets.ModelViewSet):
    queryset=Standard.objects.all()
    serializer_class=standardserializer
    permission_classes = (IsAuthenticated,)

class SubjectViewSet(viewsets.ModelViewSet):
    queryset=Subject.objects.all()
    serializer_class=SubjectSerializer
    permission_classes = (IsAuthenticated,)

class LessonViewSet(viewsets.ModelViewSet):
    queryset=Lesson.objects.all()
    serializer_class=LessonSerializer
    permission_classes = (IsAuthenticated,)