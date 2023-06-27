from django.core import serializers
from django.http import JsonResponse
from users.models import *
from django.views.decorators.csrf import csrf_exempt

@csrf_exempt
def getusers(request):
    obj=User.objects.all()
    obj1=serializers.serialize('python',obj)
    return JsonResponse(obj1,safe=False)
