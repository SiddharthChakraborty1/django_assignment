from typing import List
from django.shortcuts import render
from .models import Resource, Project, Release
from rest_framework import views, viewsets
from .serializers import ResourceSerializer, ProjectSerializer, ReleaseSerializer
from rest_framework.response import Response
from rest_framework import status
from rest_framework_bulk import ListBulkCreateUpdateDestroyAPIView

# Create your views here.

def homeView(request):
    return render(request, 'home.html')

class ResourceViewset(viewsets.ModelViewSet):
    queryset = Resource.objects.all()
    serializer_class = ResourceSerializer

    def create(self, request, *args, **kwargs):
        print('printing request data from viewset of resources')
        print(request.data)
        data = request.data
        many = isinstance(data, list)
        print(data, many)
        serializer = self.get_serializer(data=data, many = many)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        headers = self.get_success_headers(serializer.data)
        return Response(
            serializer.data,
            status = status.HTTP_201_CREATED,
            headers= headers
        )

    def update(self, request, *args, **kwargs):
        if isinstance(request.data, list):
            for data in request.data:
                if Resource.objects.filter(id = data['id']).exists():
                    user = Resource.objects.get(id = data['id'])
                    if 'project' in data.keys():
                        user.project = Project.objects.get(id = data['project'])

                    if 'project' not in data.keys():
                        user.project = Project.objects.get(name = 'Resource Pool')
                    
                    if 'name' in data.keys():
                        user.name = data['name']

                    if 'password' in data.keys():
                        user.password = data['password']
                        
                    if 'is_admin' in data.keys():
                        user.is_admin = data['is_admin']

                    if 'is_staff' in data.keys():
                        user.is_staff = data['is_staff']

                    
                    if 'is_superuser' in data.keys():
                        user.is_superuser = data['is_superuser']
                    
                    if 'experience' in data.keys():
                        user.expeirience = data['experience']

                    user.save()
                else:
                    return Response(status = status.HTTP_404_NOT_FOUND)
            
        else:
            if Resource.objects.filter(id = request.data['id']).exists():
                user = Resource.objects.get(id = request.data['id'])
                if 'project' in request.data.keys():
                        user.project = Project.objects.get(id = request.data['project'])\

                if 'project' not in request.data.keys():
                        user.project = Project.objects.get(name = 'Resource Pool')

                if 'name' in request.data.keys():
                        user.name = request.data['name']

                if 'password' in request.data.keys():
                        user.password = request.data['password']
                        
                if 'is_admin' in request.data.keys():
                        user.is_admin = request.data['is_admin']

                if 'is_staff' in request.data.keys():
                        user.is_staff = request.data['is_staff']

                    
                if 'is_superuser' in request.data.keys():
                        user.is_superuser = request.data['is_superuser']
                    
                if 'experience' in request.data.keys():
                        user.expeirience = request.data['experience']
                

                user.save()
            else:
                return Response(status = status.HTTP_404_NOT_FOUND)

        return Response({'msg': 'updated successfully'}, status = status.HTTP_204_NO_CONTENT)


class ProjectViewset(viewsets.ModelViewSet):
    queryset = Project.objects.all()
    serializer_class = ProjectSerializer

    def destroy(self, request, *args, **kwargs):
        print(kwargs)
        project_id = kwargs['pk']
        if Project.objects.filter(id = project_id).exists():
            if Project.objects.get(id = project_id).name != 'Resource Pool':
                project = Project.objects.get(id = project_id)
                project.delete()
                return Response({'message':'Project deleted successfully!'}, status = status.HTTP_200_OK)
            else:
                return Response({'message':'Cannot delete project Resource Pool'}, status=status.HTTP_400_BAD_REQUEST)
        else:
            return Response({'message':'Project does not exist'}, status = status.HTTP_404_NOT_FOUND)

class ReleaseViewset(viewsets.ModelViewSet):
    queryset = Release.objects.all()
    serializer_class = ReleaseSerializer

    def create(self, request, *args, **kwargs):
        data = request.data 
        if 'project' and 'release_date' and 'version' and 'description' in data.keys():
            if Project.objects.filter(id = data['project']).exists():
                if Project.objects.get(id = data['project']).name != 'Resource Pool':
                    release = Release.objects.create(project = Project.objects.get(id = data['project']),
                    release_date = data['release_date'], version = data['version'],
                    description = data['description'])
                    release.save()
                    return Response(status = status.HTTP_201_CREATED)
                else:
                    return Response({'message': 'Resource Pool does not accept releases'},
                    status = status.HTTP_400_BAD_REQUEST)
            else:
                return Response({'message':'Project does not exist'}, status = status.HTTP_404_NOT_FOUND)
        else:
            return Response(status = status.HTTP_400_BAD_REQUEST)
                    

    def update(self, request, *args, **kwargs):
        release_id = kwargs['pk']
        if Release.objects.filter(id = release_id).exists():
            if 'project' in request.data.keys():
                if Project.objects.filter(id = request.data['project']).exists():
                    if Project.objects.get(id = request.data['project']).name != 'Resource Pool':
                        release = Release.objects.filter(id = release_id)
                        if 'release_date' in request.data.keys():
                            release.update(release_date = request.data['release_date'])
                        if 'description' in request.data.keys():
                            release.update(description = request.data['description'])
                            return Response({'message': 'updated successfully'},
                            status = status.HTTP_200_OK)
                    else:
                        return Response({'message':'Resource Pool does not contain any releases'},
                        status = status.HTTP_400_BAD_REQUEST)
                else:
                    return Response({'message':'Project not found'}, status = status.HTTP_404_NOT_FOUND)
            else:
                return Response({'message': 'mandatory field (project) missing'}, status = status.HTTP_400_BAD_REQUEST)
        else:
            return Response({'message': 'Invalid release id'}, status=status.HTTP_404_NOT_FOUND)

