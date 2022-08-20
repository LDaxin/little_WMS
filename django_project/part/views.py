import imp
from django.shortcuts import render
from rest_framework.response import Response
from rest_framework import status
from rest_framework.decorators import api_view
from part import models
from .serializer import PartSerializer
# Create your views here.

@api_view(['GET', 'POST'])
def part(request):
    if request.method == 'GET':
        all_parts = models.Part.objects.all()
        serializer = PartSerializer(all_parts, many=True)
        return Response(serializer.data)
    elif request.method == 'POST':
        
        serializer = PartSerializer(request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
