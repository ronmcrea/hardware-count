from django.shortcuts import render, redirect
from .models import Table
from .serializers import tableSerializer
from rest_framework import status
from rest_framework.decorators import api_view
from django.http.response import JsonResponse
from rest_framework.parsers import JSONParser
from django.http import HttpResponse
from django.template import loader

# Create your views here.
@api_view(['GET','POST'])
def list(request):
    if request.method == 'GET':
        data = Table.objects.all()
        serializer = tableSerializer(data, many=True)
        return JsonResponse(serializer.data, safe=False)
    
    elif request.method == 'POST':
        print(request.POST['name'])

        newtable = Table.objects.create()
        newtable.name = request.POST['name']

        newtable.save()

        return redirect("main")
        # req_data = JSONParser().parse(request)
        # print(request)
        # serializer = tableSerializer(data=req_data)
        

        # if serializer.is_valid():
        #     serializer.save()
        #     return redirect('main')
        #     return JsonResponse(serializer.data, status=status.HTTP_201_CREATED)
        # return JsonResponse(serializer.error, status=status.HTTP_400_BAD_REQUEST)

def main(request):
  return render(request, "forms/main.html")
