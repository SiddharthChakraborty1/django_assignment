import enum
from django.db.models import fields
from rest_framework import serializers
from .models import Resource, Project, Release
from projects import models
from rest_framework_bulk import (
    BulkListSerializer,
    BulkSerializerMixin,
    
)



class ResourceSerializer(serializers.ModelSerializer):
    class Meta(object):
        model = Resource
        fields = '__all__'
        read_only_fields = ("id", "email", "date_joined")
       


class ReleaseSerializer(serializers.ModelSerializer):
    class Meta:
        model = Release
        fields = '__all__'


class ProjectSerializer(serializers.ModelSerializer):
    class Meta:
        model = Project
        fields = ['id','name', 'start_date', 'end_date']
