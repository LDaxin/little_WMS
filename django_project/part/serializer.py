from re import template
from rest_framework import serializers
from . import models

class PartSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Part
        fields = ('id', 'template', 'tag')
        
