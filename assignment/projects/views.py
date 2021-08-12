from typing import List
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


    # overriding the update() method for resource model
    # this update() method has been overridden to facilitate single as well as bulk allocation
    # and deallocation of recources to projects
    
    # for allocating multiple resources to a project, we will have to send a json array as follows
    #     [
        #     {   "id" : 14,
        #         "project": 3
        
        #     },
        #     {   "id" : 13
        #         "project": 3
        #     }
        #     {   "id" : 15,
        #         "project": 3
        #     },
    # ]

    # if the above json array is received by the update method then the resources with id 13, 14 and 15
    # will be allocated to the project with id 3

    # if we want to deallocate multiple resources from a project we just have to send a json array containing
    # id of the resources we want to deallocate from projects as follows
    #     [
        #     {   "id" : 14,
        #     },
        #     {   "id" : 13
        #     }
        #     {   "id" : 15,
        #     },
    # ]

    # if the update() method receives this json array, the resources with id 13, 14 and will be deallocated
    # from the project they were associated with and will be allocated to the default project called 'Resource Pool'


    # The update() method can also be used to update other details of single or multiple users
    # {
        # "id": 13,
        # "name": "updated name",
        # "password": "updated password",
        # "experience": updated experience,
        # "is_admin": true,
        # "is_superuser": true,
        # "is_staff": true
    # }

    # the above details of the reource with id 13 will be updated
    # note: providing id of the resource in the json object is mandatory since
    # this update() method also handles updating multiple resources and it does not use
    # the id (pk) sent as part of the url, it uses the id in the json object

    # note: the email of the resource cannot be changed after account creation since it is used
    # as the username field because the resouce model is a custom user model


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

    # The create() method has been overridden to prevent a post request
    # that creates a project with name that is already present in the database

    def create(self, request, *args, **kwargs):
        data = request.data
        already_present = False
        projects = Project.objects.all()
        for project in projects:
            if project.name == data['name']:
                already_present = True
        if already_present:
            return Response({'message': 'Project with this name is already present'},
            status = status.HTTP_400_BAD_REQUEST)
        else:
            return super().create(request, *args, **kwargs)

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

    # The create() method of the Release viewset has been overridden so nobody can add
    # a release to the 'Resource Pool' project since it is the default project and hence
    # does not accept any releases

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
                    

    # The update() method of the Release viewset has been overriden to prevent people
    # from updating the version of the release and to prevent associating the release
    # to a different project

    # This update() method only allows updating the release_date and the description (deliverables)
    # of the release

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


@api_view(['GET'])
def project_release_view(request, **kwargs):
    project_id = kwargs['project_id']
    releases = Release.objects.filter(project = Project.objects.get(id = project_id))
    serializer = ReleaseSerializer(releases, many = True)
    return Response({"status": "OK",
    "data": serializer.data}, status = status.HTTP_200_OK)




