from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
import time
from django.contrib.auth.models import User
from django.db import IntegrityError
from django.contrib.auth import login, logout, authenticate
from django.http import HttpResponse
from .forms import TaskForm
from .models import Task
from django.contrib.auth.decorators import login_required
from django.http import HttpResponseNotFound, Http404
from django.utils import timezone


# Create your views here.


def home(request):
    return render(request, "home.html")


def signup(request):
    if request.method == "GET":
        return render(
            request,
            "signup.html",
            {"form": UserCreationForm},  # Crea un formulario para un usuario
        )
    else:
        if request.POST["password1"] == request.POST["password2"]:
            try:
                user = User.objects.create_user(
                    username=request.POST["username"],
                    password=request.POST["password1"],
                )
                user.save()
                login(request, user)
                return redirect("tasks")
            except IntegrityError:
                return render(
                    request,
                    "signup.html",
                    {
                        "form": UserCreationForm,
                        "error": "Usuario ya existe",  # Crea un formulario para un usuario
                    },
                )

        return render(
            request,
            "signup.html",
            {"form": UserCreationForm, "error": "Contraseñas, no coinside"},
        )


@login_required
def tasks(request):
    # Filtra las tareas por user,
    tasks = Task.objects.filter(user=request.user, datecompleted__isnull=True)
    print(tasks)
    return render(request, "tasks.html", {'tasks': tasks})


@login_required
def tasks_completed(request):
    tasks = Task.objects.filter(
        user=request.user, datecompleted__isnull=False).order_by
    ('-datecreated')  # Ordena de mas reciente a mas antigua
    print(tasks)
    return render(request, "tasks.html", {'tasks': tasks})


def close(request):
    logout(request)
    return redirect("home")


def signin(request):
    if request.method == "GET":
        return render(request, "signin.html", {"form": AuthenticationForm})
    else:
        user = authenticate(
            request,
            username=request.POST["username"],
            password=request.POST["password"],
        )
    if user is None:
        return render(
            request,
            "signin.html",
            {"form": AuthenticationForm, "error": "!Usuario contraseña incorrecta¡"},
        )
    else:
        login(request, user)
        return redirect("tasks")


@login_required
def create_task(request):
    if request.method == "GET":
        return render(request, 'create_task.html', {
            'form': TaskForm
        })
    else:
        try:
            form = TaskForm(request.POST)
            # No queremos que guarde la data
            new_task = form.save(commit=False)
            new_task.user = request.user
            new_task.save()
            print(new_task)
            return redirect('task')
        except ValueError:
            return render(request, 'create_task.html', {
                'form': TaskForm,
                'error': '¡Error al crear tarea!'
            })

@login_required
def task_detail(request, task_id):
    try:
        task = get_object_or_404(Task, pk=task_id, user=request.user)
        if request.method == 'POST':
            # Obtenemos un formulario para actualizar la task
            form = TaskForm(request.POST, instance=task)
            if form.is_valid():
                form.save()
            return redirect('tasks')
        else:
            form = TaskForm(instance=task)
        return render(request, 'task_detail.html', {'task': task, 'form': form})
    except Http404:
        return render(request, '404.html',  status=404)

@login_required
def complete_task(request, task_id):
    task = get_object_or_404(Task, pk=task_id, user=request.user)
    if request.method == 'POST':
        task.datecompleted = timezone.now()
        task.save()

    return redirect('tasks')

@login_required
def delete_task(request, task_id):
    task = get_object_or_404(Task, pk=task_id, user=request.user)
    if request.method == 'POST':
        task.delete()
    return redirect('tasks')
