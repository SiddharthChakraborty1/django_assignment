"""assignment URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django import urls
from django.conf.urls import url
from django.contrib import admin
from django.urls import path, include
from projects import views as projectsView
from rest_framework.routers import DefaultRouter
from projects.views import ResourceViewset, ProjectViewset, ReleaseViewset, project_release_view, allocate_resources_view, deallocate_resource_view
from rest_framework_bulk.routes import BulkRouter


router = DefaultRouter()
bulk_router = BulkRouter()
router.register('user',ResourceViewset,basename='user')
router.register('project', ProjectViewset, basename='project')
router.register('release', ReleaseViewset, basename='release' )

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', projectsView.homeView),
    path('api/', include(router.urls)),
    path('api/project/releases/<project_id>/', project_release_view, name='project release view'),
    path('api/allocateResources/<project_id>/', allocate_resources_view, name='allocate resources to project'),
    path('api/deallocateResources/', deallocate_resource_view, name='deallocate resources from project')

]