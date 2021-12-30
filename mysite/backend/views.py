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

class Compute(GenericAPIView):
    def post(request:HttpRequest):
        data = JSONParser.parse(request) if request.data is str else request.data
        if not data.__contains__("matrix1") or not data.__contains__("numRows1") or not data.__contains__("numCols1"):
            return HttpResponseBadRequest()
        if not data.__contains__("matrix2") or not data.__contains__("numRows2") or not data.__contains__("numCols2"):
            return HttpResponseBadRequest()
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