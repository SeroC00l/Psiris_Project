from .forms import LoginForm, RegisterForm
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from django.views.decorators.http import require_http_methods
from django.http import HttpResponseNotAllowed
from django.contrib import messages
from .models import Task, TodoList
from .forms import TaskForm, TodoListForm, RegisterForm, LoginForm, EditTaskForm
from typing import List


def user_login(request):
    if request.method == 'POST':
        form = LoginForm(request.POST)
        if form.is_valid():
            cd = form.cleaned_data
            user = authenticate(
                request, username=cd['username'], password=cd['password'])
            if user is not None:
                login(request, user)
                return redirect('home/')
            else:
                error = 'User or Password is incorrect'
    else:
        form = LoginForm()
        error = None
    return render(request, 'login.html', {'form': form, 'error': error})


def register(request):
    errors = []
    if request.method == 'POST':
        form = RegisterForm(request.POST)
        if form.is_valid():
            cd = form.cleaned_data
            user = User.objects.create_user(
                username=cd['username'],
                email=cd['email'],
                password=cd['password1']
            )
            login(request, user)
            return redirect('/home/')
        else:
            errors = form.errors.values()
    else:
        form = RegisterForm()
    return render(request, 'register.html', {'form': form, 'error': errors})


def logout_view(request):
    logout(request)
    return redirect('/')

@login_required
def home(request, list_id=None):
    todo_lists = TodoList.objects.filter(user=request.user).order_by('-id')
    list_form = TodoListForm()
    if not todo_lists.exists():
        return render(request, 'no_lists.html', { 'list_form': list_form })

    if list_id is None:
        list_id = todo_lists.first().id
    else:
        list_id = int(list_id)

    todo_list = get_object_or_404(TodoList, id=list_id, user=request.user)
    todo_items = Task.objects.filter(todo_list=todo_list)
    list_form = TodoListForm()
    selected_list = request.GET.get('list_id')
    if selected_list:
        selected_list = get_object_or_404(TodoList, id=selected_list, user=request.user)
        tasks = Task.objects.filter(todo_list=selected_list).order_by('-id')
    else:
        selected_list = None
        tasks = None
        list_form = TodoListForm()

    if request.method == 'POST':
        task_form = TaskForm(request.POST)
        list_id = request.POST.get('todo_list')
        if task_form.is_valid():
            new_task = task_form.save(commit=False)
            new_task.todo_list = TodoList.objects.get(id=list_id)
            new_task.save()
            return redirect('/home/', list_id=todo_list.id)
        else:
            print(task_form.errors)
    else:
        list_id = request.POST.get('list_id')
        task_form = TaskForm(initial={'todo_list': todo_list.id})

    return render(request, 'home.html', {'todo_list': todo_list, 'todo_items': todo_items, 'list_form': list_form, 'lists': todo_lists, 'selected_list': selected_list, 'tasks': tasks,'task_form': task_form})


@login_required
def create_list(request):
    if request.method == 'POST':
        form = TodoListForm(request.POST)
        if form.is_valid():
            todo_list = form.save(commit=False)
            todo_list.user = request.user
            todo_list.save()
            return redirect('/home/')
    else:
        form = TodoListForm()
    return render(request, 'tasks/home.html', {'list_form': form})


@login_required
def edit_task(request, list_id, task_id):
    task = get_object_or_404(Task, id=task_id)
    if request.method == 'POST':
        form = EditTaskForm(request.POST, instance=task)
        if form.is_valid():
            task = form.save(commit=False)
            task.todo_list_id = task.todo_list.id
            task.save()
            return redirect('/home/')
    else:
        form = TaskForm(instance=task)

    return render(request, 'edit_task.html', {'task_form': form})


@login_required
def delete_task(request, list_id, task_id):
    task = get_object_or_404(Task, id=task_id)
    task.delete()
    return redirect('/home/')

@login_required
def edit_list(request, list_id):
    todo_list = get_object_or_404(TodoList, id=list_id)
    print(request.POST)
    if request.method == 'POST':
        form = TodoListForm(request.POST, instance=todo_list)
        if form.is_valid():
            todo_list = form.save(commit=False)
            todo_list.user = request.user
            todo_list.id = list_id
            todo_list.save()
            return redirect('/home/')
    else:
        form = TodoListForm(instance=todo_list)
    return render(request, 'edit_list.html', {'list_form': form})



@login_required
def delete_list(request):
    if request.method == 'POST':
        print(request.POST)
        list_id = request.POST.get('list_id')
        list = get_object_or_404(TodoList, id=list_id)
        list.delete()
        return redirect('/home/')
    else:
        return HttpResponseNotAllowed(['POST'])
