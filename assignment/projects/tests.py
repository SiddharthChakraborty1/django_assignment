from django.test import TestCase
from rest_framework import VERSION, response
import rest_framework
from rest_framework.test import APITestCase, APIClient
from rest_framework.response import Response
from rest_framework import status
from .models import Project, Resource, Release

# Create your tests here.
class ProjectAPITestCase(APITestCase):
    def setUp(self):
        self.client = APIClient()
        self.project = Project.objects.create(name='dummy project 1', start_date='2021-08-13',
        end_date = '2022-08-13')
        self.project.save()

    def test_createProject(self):
        count1 = Project.objects.all().count()
        Project_dict = dict(name='dummy project',
        start_date='2021-08-13', end_date='2024-08-13')
        response = self.client.post('/api/project/', Project_dict)
        count2 = Project.objects.all().count()
        self.assertEqual(response.status_code,status.HTTP_201_CREATED)
        self.assertEqual(count1+1, count2)

    def test_updateProject(self):
        project_id = self.project.id 
        project_dict = dict(name = 'updated name',
        start_date = '2021-08-13', end_date='2022-08-13')
        response = self.client.put(f'/api/project/{project_id}/', project_dict)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        project = Project.objects.get(id = project_id)
        self.assertEqual(project.name,'updated name')

    def test_getProject(self):
        project_id = self.project.id 
        response = self.client.get(f'/api/project/{project_id}/')
        self.assertEqual(response.data['name'], self.project.name)
    
    def test_deleteProject(self):
        
        pro = Project.objects.create(name='project dummy', start_date='2021-09-20',
        end_date = '2023-09-20')
        pro.save()
        count1 = Project.objects.all().count()
        response = self.client.delete(f'/api/project/{pro.id}/')
        count2 = Project.objects.all().count()
        self.assertEqual(count1 - 1, count2)


class ResourceAPITestCase(APITestCase):
    def setUp(self):
        self.default_project = Project.objects.create(name='Resource Pool', start_date='2021-09-20',
        end_date = '2023-09-20')
        self.default_project.save()
        self.project = Project.objects.create(name='Zipari', start_date='2021-09-20',
        end_date = '2023-09-20')
        self.project.save()

        self.user = Resource.objects.create(email = 'dummy@gmail.com', name='dummy user', experience = 1,
        password = 'abc123', project = self.default_project)
        self.user.save()
        self.client = APIClient()

    def test_createUser(self):
        count1 = Resource.objects.all().count()
        user_dict = dict(name='dummy user 2', email = 'dummyUser@gmail.com',
        password = 'abc123', experience = 2, project = self.default_project.id)
        response = self.client.post('/api/user/',user_dict)
        count2 = Resource.objects.all().count()
        self.assertEqual(count1+1, count2)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_getUser(self):
        user_id = self.user.id 
        response = self.client.get(f'/api/user/{user_id}/')
        self.assertEqual(self.user.name, response.data['name'])

    def test_updateUser(self):
        user_id = self.user.id 
        user_dict = dict(name='updated name', email = self.user.email,
        password = self.user.password, experience = self.user.experience, project = self.default_project.id)
        response = self.client.put(f'/api/user/{user_id}/', user_dict)
        response = self.client.get(f'/api/user/{user_id}/')
        self.assertEqual(response.data['name'], 'updated name')

    def test_deleteUser(self):
        user_id = self.user.id
        count1 = Resource.objects.all().count()
        response = self.client.delete(f'/api/user/{user_id}/')
        count2 = Resource.objects.all().count()
        self.assertEqual(count1-1, count2)

class ReleaseAPITestCase(APITestCase):
    def setUp(self) -> None:
        self.client = APIClient()
        self.project = Project.objects.create(name='Zipari', start_date='2021-09-20',
        end_date = '2023-09-20')
        self.project.save()
        
        self.release = Release.objects.create(version = 0.1, project = self.project, description = 'dummy description',
        release_date = '2021-08-15')
        self.release.save()


    def test_createRelease(self):
        release_dict = dict(description = 'dummy description',
        release_date = '2022-8-19', version = 0.1, project = self.project.id)
        response = self.client.post('/api/release/', release_dict)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_updateRelease(self):
        release_id = self.release.id 
        release_dict = dict(description = 'updated description')
        response = self.client.put(f'/api/release/{self.release.id}/', release_dict)
        response = self.client.get(f'/api/release/{self.release.id}/')
        self.assertEqual(response.data['description'], 'updated description')

    def test_deleteRelease(self):
        count1 = Release.objects.all().count()
        response = self.client.delete(f'/api/release/{self.release.id}/')
        count2 = Release.objects.all().count()
        self.assertEqual(count1-1, count2)


        

        


        

