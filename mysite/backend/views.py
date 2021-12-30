from django.shortcuts import render

# Create your views here.
import json
from django.http.request import HttpRequest
from django.http.response import Http404, HttpResponse, HttpResponseBadRequest, HttpResponseForbidden, HttpResponseNotFound, JsonResponse
from rest_framework import status
from rest_framework.generics import GenericAPIView
from rest_framework.response import Response
from rest_framework.parsers import JSONParser

class ReceiveInput(GenericAPIView):
    def post(request:HttpRequest):
        data = JSONParser.parse(request) if request.data is str else request.data
        