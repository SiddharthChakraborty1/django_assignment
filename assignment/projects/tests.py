from django.test import TestCase
from rest_framework import response
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


        

