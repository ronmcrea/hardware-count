# from django.shortcuts import render
# from django.db.models import Prefetch
# # Create your views here.
# from rest_framework import viewsets
# from .models import Stock, Borrow
# from .serializers import StockSerializer, BorrowSerializer

# class StockViewSet(viewsets.ModelViewSet):
#     serializer_class = StockSerializer
#     queryset = Stock.objects.all()

# class BorrowViewSet(viewsets.ModelViewSet):
#     serializer_class = BorrowSerializer
#     queryset = Borrow.objects.all()
from datetime import date
from django.shortcuts import render
from django.db import transaction
from django.http.response import JsonResponse
from rest_framework.parsers import JSONParser 
from rest_framework import status
from .models import Stock, Borrow
from .serializers import StockSerializer, BorrowSerializer
from rest_framework.decorators import api_view
from django.http import HttpResponse

@api_view(['GET', 'POST', 'UPDATE'])
def stock_list(request):
    if request.method == 'GET':
        stocks = Stock.objects.all()
        stocks_serializer = StockSerializer(stocks, many=True)
        return JsonResponse(stocks_serializer.data, safe=False)
        # 'safe=False' for objects serialization
 
    elif request.method == 'POST':
        stock_data = JSONParser().parse(request)
        stock_serializer = StockSerializer(data=stock_data)
        if stock_serializer.is_valid():
            stock_serializer.save()
            return JsonResponse(stock_serializer.data, status=status.HTTP_201_CREATED) 
        return JsonResponse(stock_serializer.errors, status=status.HTTP_400_BAD_REQUEST)

@api_view(['GET', 'POST'])
def borrow_list(request):
    if request.method == 'GET':
        borrows = Borrow.objects.all()
        borrows_serializer = BorrowSerializer(borrows, many=True)
        return JsonResponse(borrows_serializer.data, safe=False)
 
    elif request.method == 'POST':

        borrow_data = JSONParser().parse(request)
        borrow_serializer = BorrowSerializer(data=borrow_data)

        stocks = Stock.objects.get(itemName = borrow_data["itemName"])

        if(stocks.quantity >= borrow_data["quantity"]):
            stocks.quantity = stocks.quantity - borrow_data["quantity"]
        else:
            return JsonResponse(borrow_serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        
        if borrow_serializer.is_valid():
            borrow_serializer.save()
            stocks.save()
            return JsonResponse(borrow_serializer.data, status=status.HTTP_201_CREATED) 
        return JsonResponse(borrow_serializer.errors, status=status.HTTP_400_BAD_REQUEST)

@api_view(['POST'])
def return_list(request):
    if request.method == 'POST':

        return_data = JSONParser().parse(request)

        borrows = Borrow.objects.get(id = return_data["id"])
        borrows.returnedDate=date.today()
        borrows.status="Returned"
        borrows.save()
        
        stocks = Stock.objects.get(itemName = return_data["itemName"])
        stocks.quantity = stocks.quantity + return_data["quantity"]
        stocks.save()

        return HttpResponse("Test")