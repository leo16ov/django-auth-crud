"""
URL configuration for djangocrud project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.0/topics/http/urls/
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
from django.contrib import admin
from django.urls import path
from Tasks import views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', views.home),
    path('signup/',views.signup),
    path('tasks/', views.tasks),
    path('tasks/create/', views.createTask),
    path('signout/', views.signout),
    path('login/', views.signin),
    path('tasks/<int:id_task>/', views.detailsTask, name= 'task_details'),
    path('tasks/<int:id_task>/complete/', views.completeTask, name= 'task_complete'),
    path('tasks/<int:id_task>/delete/', views.deleteTask, name= 'task_delete'),

]
