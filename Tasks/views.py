from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth.models import User
from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse
from django.db import IntegrityError
from django.utils import timezone
from .forms import CreateTaskForm
from .models import Task

# Create your views here.

def home(request):
    return render(request, 'home.html')

@login_required
def tasks(request):
    tasks = Task.objects.filter(user = request.user, datecomplete__isnull= True)
    return render(request, 'tasks.html',{
        'tasks': tasks
    })

@login_required
def createTask(request):
    if request.method == 'GET':
        return render(request, 'create_task.html', {
            'form': CreateTaskForm
        })
    else:
        try:
            form = CreateTaskForm(request.POST)
            newTask = form.save(commit= False)
            newTask.user = request.user
            newTask.save()

            return redirect('/tasks/')
        except:
            return render(request, 'create_task.html', {
                'form': CreateTaskForm,
                'error': 'Error inesperado'
            })

@login_required
def detailsTask(request, id_task):
    if request.method == 'GET':
        task = get_object_or_404(Task, pk= id_task, user= request.user, datecomplete__isnull= True)
        form = CreateTaskForm(instance= task)
        return render(request, 'task_details.html', {
            'task': task,
            'form': form
        })
    else:
        try:
            task = get_object_or_404(Task, pk= id_task, user= request.user, datecomplete__isnull= True)
            form = CreateTaskForm(request.POST, instance= task)
            form.save()
            return redirect('/tasks/')
        except ValueError:
            return render(request, 'task_details.html', {
            'task': task,
            'form': form
        })

@login_required
def completeTask(request, id_task):
    if request.method == 'POST':
        task = get_object_or_404(Task, pk= id_task, user= request.user, datecomplete__isnull=  True)
        task.datecomplete = timezone.now()
        task.save()
        return redirect('/tasks/')

@login_required
def deleteTask(request, id_task):
    if request.method == 'POST':
        task = get_object_or_404(Task, pk= id_task, user= request.user)
        task.delete()
        return redirect('/tasks/')

def signup(request):
    if request.method == 'GET':
        return render(request, 'signup.html', {
            'form': UserCreationForm
        })
    
    else:
        if request.POST['password1'] == request.POST['password2']:
            try:
                print(request.POST)
                print(request.POST['username'])
                user = User.objects.create_user(username= request.POST['username'], password= request.POST['password1'])
                user.save()
                login(request, user)
                return redirect('/tasks/')

            except IntegrityError:
                return render(request, 'signup.html', {
                    'form': UserCreationForm,
                    'error': 'El username ya esta en uso'
                })

        elif request.POST['password1'] != request.POST['password2']:
            return render(request, 'signup.html', {
                'form': UserCreationForm,
                'error': 'Las contraseñas no coinciden, intentelo de nuevo'
            })

@login_required
def signout(request):
    logout(request)
    return redirect('/')

def signin(request):
    if request.method == 'GET':
        return render(request, 'login.html', {
            'form': AuthenticationForm
        })
    else: 
        user = authenticate(
            request, username= request.POST['username'], password = request.POST['password']
            )
        if user is None:
            return render(request, 'login.html', {
                'form': AuthenticationForm,
                'error': 'El usuario o contraseña son incorrectos'
            })
        else:
            login(request, user)
            return redirect('/tasks/')

