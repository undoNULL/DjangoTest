#from django.shortcuts import render

# Create your views here.

from django.http import JsonResponse

#def hello(request):
#    return JsonResponse({"msg":"world"})

def hello(request):
    version = request.GET.get('v', 'world')
    return JsonResponse({"msg": version})