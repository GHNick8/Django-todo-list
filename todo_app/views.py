from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required

from django.utils.timezone import now
from datetime import date

from .models import Task
from .forms import TaskForm

@login_required
def task_list(request):
    filter_option = request.GET.get('filter')
    tasks = Task.objects.filter(user=request.user).order_by('-created_at')
    today = date.today()

    if filter_option == "completed":
        tasks = tasks.filter(completed=True)
    elif filter_option == "pending":
        tasks = tasks.filter(completed=False)
    elif filter_option == "high":
        tasks = tasks.filter(priority="High")
    elif filter_option == "medium":
        tasks = tasks.filter(priority="Medium")
    elif filter_option == "low":
        tasks = tasks.filter(priority="Low")
    
    return render(request, 'todo_app/task_list.html', {'tasks': tasks, 'today': today})

@login_required
def task_create(request):
    if request.method == 'POST':
        form = TaskForm(request.POST)
        if form.is_valid():
            task = form.save(commit=False)
            task.user = request.user
            task.save()
            return redirect('task_list')
        
    else:
        form = TaskForm()
    return render(request, 'todo_app/task_form.html', {'form': form})

@login_required
def task_update(request, task_id):
    task = get_object_or_404(Task, id=task_id, user=request.user)
    if request.method == "POST":
        form = TaskForm(request.POST, instance=task)
        if form.is_valid():
            form.save()
            return redirect('task_list')
    else:
        form = TaskForm(instance=task)
    return render(request, 'todo_app/task_form.html', {'form': form})

@login_required
def task_delete(request, task_id):
    task = get_object_or_404(Task, id=task_id, user=request.user)
    if request.method == "POST":
        task.delete()
        return redirect('task_list')
    return render(request, 'todo_app/task_confirm_delete.html', {'task': task})
