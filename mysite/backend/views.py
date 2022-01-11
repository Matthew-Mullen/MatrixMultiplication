from django.shortcuts import render

# Create your views here.
import json
from django.http.request import HttpRequest
from django.http.response import Http404, HttpResponse, HttpResponseBadRequest, HttpResponseForbidden, HttpResponseNotFound, JsonResponse
from rest_framework import status
from rest_framework.generics import GenericAPIView
from rest_framework.response import Response
from rest_framework.parsers import JSONParser
import numpy
from models import Account, StockOfPortfolio

class Compute(GenericAPIView):
    def post(request:HttpRequest, op:str):
        data = JSONParser.parse(request) if request.data is str else request.data
        if not data.__contains__("matrix1") or not data.__contains__("numRows1") or not data.__contains__("numCols1"):
            return HttpResponseBadRequest()
        if not data.__contains__("matrix2") or not data.__contains__("numRows2") or not data.__contains__("numCols2"):
            return HttpResponseBadRequest()
        if op=="mult":
            matrix1=data["matrix1"]
            numRows1=data["numRows1"]
            numCols1=data["numCols1"]
            matrix2=data["matrix2"]
            numRows2=data["numRows2"]
            numCols2=data["numCols2"]
            if numCols1!=numRows2:
                return HttpResponseBadRequest("Incorrect matrix dimensions")
            intMat1 = numpy.array([map(int,i) for i in matrix1])
            intMat2 = numpy.array([map(int,i) for i in matrix2])
            res=numpy.matmul(intMat1,intMat2).tolist()
            data={'result':res}
            return Response(json.dumps(data),status=200)
class Portfolio(GenericAPIView):
    def get(request:HttpRequest, user_id:str):
        data = JSONParser.parse(request) if request.data is str else request.data
        account = Account(id=user_id)
        if not account:
            return HttpResponseNotFound()
        stocks = StockOfPortfolio(filter(owner=account))
        return HttpResponse(json.dumps(stocks),status=200)

    def post(request:HttpRequest, user_id:str):
        data = JSONParser.parse(request) if request.data is str else request.data
        stock_id=data["stock_id"]
        op=data["op"]
        quantity=data["quantity"]
        price=data["price"]
        account = Account(id=user_id)
        if not account:
            return HttpResponseNotFound()
        stock = StockOfPortfolio(filter(owner=account, tag=stock_id))
        if not stock:
            stock=StockOfPortfolio.objects.create(tag=stock_id, owner=account)
        if op=="BUY":
            account.money-=(price*quantity)
            stock.quantityOwned+=quantity
        elif op=="SELL":
            account.money+=(price*quantity)
            stock.quantityOwned-=quantity
        stock.save()
        account.save()
        return HttpResponse(status=200)