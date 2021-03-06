import datetime
from typing import KeysView, List
from django.db.models.fields import DateTimeCheckMixin
from django.shortcuts import render
from rest_framework.generics import UpdateAPIView
from rest_framework import response
from .models import Resource, Project, Release
from rest_framework.decorators import api_view
from rest_framework import views, viewsets
from .serializers import ResourceSerializer, ProjectSerializer, ReleaseSerializer
from rest_framework.response import Response
from rest_framework import status
from rest_framework_bulk import ListBulkCreateUpdateDestroyAPIView
from datetime import date, datetime

# Create your views here.




def homeView(request):
    return render(request, 'home.html')

class ResourceViewset(viewsets.ModelViewSet):
    queryset = Resource.objects.all()
    serializer_class = ResourceSerializer

    

    # the following create() method can accept either a single json object and create
    # a single resource or it can accept a json array containing multiple json objects
    # and create multiple resources

    # the structure of json array for creating multiple resources is as follows
    #     [
        #     {   
        #     "email": "s.chakraborty2@globallogic.com",
        #     "experience": 1,
        #     "name": "Siddharth Chakraborty",
        #     "password": "abc123"
        #     },
        #     {   
        #     "email": "utkarsh@gmail.com",
        #     "experience": 1,
        #     "name": "Utkarsh Koshta",
        #     "password": "def123",
        #     "project": 3
        # }
    # ]

    #if while creating a resource
    #the project is not specified, then the resource will be associated with a 
    #default project called 'Resource Pool'

    def create(self, request, *args, **kwargs):
       
        data = request.data
        many = isinstance(data, list)
       
        serializer = self.get_serializer(data=data, many = many)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        headers = self.get_success_headers(serializer.data)
        return Response(
            serializer.data,
            status = status.HTTP_201_CREATED,
            headers= headers
        )


    # The update() method of the resource viewset has been overridden
    # to prevent updation of email field since it is used for auth purposes
    
    

    def update(self, request, *args, **kwargs):
        resource_id = kwargs['pk']
        try:
            user = Resource.objects.get(id = resource_id)
        except Resource.DoesNotExist:
            user = None
        if user is not None:
            if request.data.get('email') != user.email:
                return Response({"Message": "Cannot update email after account creation"},
                status = status.HTTP_400_BAD_REQUEST)
            else:
                return super().update(request, *args, **kwargs)
            
        else:
            return Response({"Message": "User not found"},
            status = status.HTTP_404_NOT_FOUND)

        


class ProjectViewset(viewsets.ModelViewSet):
    queryset = Project.objects.all()
    serializer_class = ProjectSerializer

    # The create() method has been overridden to prevent a post request
    # that creates a project with name that is already present in the database

    def create(self, request, *args, **kwargs):
        project, created = Project.objects.get_or_create(name = request.data['name'], defaults={'start_date': request.data['start_date'],
        'end_date': request.data['end_date']})
        if created:
            return Response({'Message': 'Created successfully'}, status = status.HTTP_201_CREATED)
        else:
            return Response({'Message': f'Project with the given name already exists'}, status = status.HTTP_400_BAD_REQUEST)

    # The update method is overridden to prevent any changes to 
    # the Resource Pool project

    def update(self, request, *args, **kwargs):
        project_id = kwargs['pk']
        if Project.objects.get(id = project_id).name == 'Resource Pool':
            return Response({'message':'Resource Pool cannot be updated'},
            status = status.HTTP_400_BAD_REQUEST)
        else:
            return super().update(request, *args, **kwargs)

    # The destroy() method of the Project viewset has been overriden so nobody can
    # delete the 'Resource Pool' project since it is the default project for any resource
    # that is not yet allocated to a project

    def destroy(self, request, *args, **kwargs):
       
        project_id = kwargs['pk']
        try:
            project = Project.objects.get(id = project_id)
        except Project.DoesNotExist:
            project = None
        if project is not None:
            if project.name != 'Resource Pool':
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

    # The create() method of the Release viewset has been overridden so nobody can add
    # a release to the 'Resource Pool' project since it is the default project and hence
    # does not accept any releases

    def create(self, request, *args, **kwargs):
        data = request.data 
        if 'project' in data.keys() and 'release_date' in data.keys() and 'version' in data.keys()   and 'description' in data.keys():
            try:
                project = Project.objects.get(id = data['project'])
            except Project.DoesNotExist:
                project = None
            if project is not None:
                sent_date = datetime.strptime(data['release_date'], '%Y-%m-%d')
                today = datetime.now()
                timeData = sent_date - today
               
                if timeData.days >= 1:
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
                    return Response({'Message': 'Invalid future release date'},
                    status = status.HTTP_400_BAD_REQUEST)
            else:
                return Response({'message':'Project does not exist'}, status = status.HTTP_404_NOT_FOUND)
        else:
            return Response(status = status.HTTP_400_BAD_REQUEST)
                    

    # The update() method of the Release viewset has been overriden to prevent people
    # from updating the version of the release and to prevent associating the release
    # to a different project

    # This update() method only allows updating the release_date and the description (deliverables)
    # of the release

    def update(self, request, *args, **kwargs):
        release_id = kwargs['pk']
        try:
            release = Release.objects.get(id = release_id)
        except Release.DoesNotExist:
            release = None
        if release is not None:
            if 'description' in request.data.keys() or 'release_date' in request.data.keys():
                release = Release.objects.filter(id = release_id)
                if 'release_date' in request.data.keys():
                    release.update(release_date = request.data['release_date'])
                if 'description' in request.data.keys():
                    release.update(description = request.data['description'])
                return Response({'message': 'updated successfully'},
                status = status.HTTP_200_OK)
            else:
                return Response({'Message': 'Only description and release_date can be updated'},
                status = status.HTTP_400_BAD_REQUEST)
                    
        else:
            return Response({'message': 'Invalid release id'}, status=status.HTTP_404_NOT_FOUND)


# The following api view takes the project id from the url
# and returns all the releases associated with that project

@api_view(['GET'])
def project_release_view(request, **kwargs):
    project_id = kwargs['project_id']
    releases = Release.objects.filter(project = Project.objects.get(id = project_id))
    serializer = ReleaseSerializer(releases, many = True)
    return Response({"status": "OK",
    "data": serializer.data}, status = status.HTTP_200_OK)

# The following api view takes project id from the url
# and it takes the id of resources as json array of objects as follows
# [{"id": 12}, {"id": 13}, {"id":14}]
# then it will allocate the resources with id 12, 13 and 14 to the project
# whoes id is sent as a part of the url

@api_view(['POST'])
def allocate_resources_view(request, **kwargs):
    project_id = kwargs['project_id']
    data = request.data
    try:
        project = Project.objects.get(id = project_id)
    except:
        project = None

    
    if project is not None:
        if project.name != 'Resource Pool':
            project = Project.objects.get(id = project_id)
            for user in data:
                if Resource.objects.filter(id = user['id']).exists():
                    resource = Resource.objects.filter(id = user['id'] )
                    resource.update(project = project)
                else:
                    return Response({'message': 'Resource not found'},
                    status = status.HTTP_404_NOT_FOUND)
            return Response({'Message':'All Resources have been allocated to the project'},
            status = status.HTTP_200_OK)
        else:
            return Response({'Message': 'Cannot explicitely allocate resources to Resource Pool'},
            status = status.HTTP_400_BAD_REQUEST)
    else:
        return Response({'Message': 'Project not found'},
        status = status.HTTP_404_NOT_FOUND)

# The following api will take id of the resources that need to be deallocated
# from their current project and will allocate them to the default project "Resource Pool"

# For example if the json array sent is as follows [{"id": 12}, {"id": 13}, {"id":14}]
# then the resources with id 12, 13 and 14 will be deallocated from whatever project they
# are working on now and will be allocated to the default project "Resource Pool"

@api_view(['POST'])
def deallocate_resource_view(request):
    default_project = Project.objects.get(name='Resource Pool')
    data = request.data
    for user in data:
        if Resource.objects.filter(id = user['id']).exists():
            resource = Resource.objects.filter(id = user['id'] )
            resource.update(project = default_project)
        else:
            return Response({'message': 'Resource not found'},
            status = status.HTTP_404_NOT_FOUND)
    return Response({'Message':'All Resources have been deallocated from the project'},
    status = status.HTTP_200_OK)
    



