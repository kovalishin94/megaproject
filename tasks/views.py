from django.shortcuts import render, redirect, get_object_or_404
from django.urls import reverse_lazy
from django.http import Http404
from django.contrib.auth.decorators import login_required
from django.db.models import Q
from django.core.exceptions import PermissionDenied
from userprofiles.models import Privilege
from .forms import TaskAddForm, TaskAnswerForm
from .models import Task
from staff.models import Employee
from datetime import datetime

# Вывод данных


@login_required(login_url=reverse_lazy('auth'))
def tasks(request):
    context = {}
    context['title'] = 'Созданные задачи'
    context['privileges'] = request.user.profile.get_plist()
    context['cur_date'] = datetime.now()
    if 'T' not in context['privileges']:
        return redirect('newtasks')
    try:
        context['tasks'] = Task.objects.filter(created_who=request.user.profile.employee).exclude(status='S').select_related(
            'target_employee').order_by('-updated_at')
    except:
        return redirect('home')
    return render(request, 'tasks/mytasks.html', context)


@login_required(login_url=reverse_lazy('auth'))
def solvedtasks(request):
    context = {}
    context['title'] = 'Решенные задачи'
    context['privileges'] = request.user.profile.get_plist()
    try:
        context['tasks'] = Task.objects.filter(Q(created_who=request.user.profile.employee) | Q(target_employee=request.user.profile.employee) | Q(delegated_employee=request.user.profile.employee), status='S').select_related(
            'target_employee', 'created_who').order_by('-updated_at')
    except:
        return redirect('home')
    return render(request, 'tasks/solvedtasks.html', context)


@login_required(login_url=reverse_lazy('auth'))
def newtasks(request):
    try:
        employee = request.user.profile.employee
    except:
        return redirect('home')
    context = {}
    context['title'] = 'Поступившие задачи'
    context['privileges'] = request.user.profile.get_plist()
    context['cur_date'] = datetime.now()
    context['tasks'] = Task.objects.filter(Q(status='C', target_employee=employee, delegated_employee=None) | Q(
        status='D', delegated_employee=employee)).select_related('target_employee')
    if request.method == 'GET':
        privilege_t = Privilege.objects.get(title='T')
        context['delegate_list'] = Employee.objects.exclude(
            pk=employee.pk).exclude(profile__privileges=privilege_t.pk)
    if request.method == 'POST':
        if 'TD' not in context['privileges']:
            raise PermissionDenied
        if not request.POST['delegated_employee']:
            return redirect('newtasks')
        cur_task = get_object_or_404(Task, pk=request.POST['taskpk'])
        cur_delegeted_employee = get_object_or_404(
            Employee, pk=request.POST['delegated_employee'])
        cur_task.delegated_employee = cur_delegeted_employee
        cur_task.status = 'D'
        cur_task.save()
        return redirect('delegatedtasks')
    return render(request, 'tasks/newtasks.html', context)


@login_required(login_url=reverse_lazy('auth'))
def acceptedtasks(request):
    context = {}
    context['title'] = 'Принятые задачи'
    context['privileges'] = request.user.profile.get_plist()
    context['cur_date'] = datetime.now()
    try:
        context['tasks'] = Task.objects.filter(Q(target_employee=request.user.profile.employee, delegated_employee=None) | Q(
            delegated_employee=request.user.profile.employee)).exclude(Q(status='C') | Q(status='S') | Q(status='D')).select_related('created_who')
    except:
        return redirect('home')
    return render(request, 'tasks/acceptedtasks.html', context)


@login_required(login_url=reverse_lazy('auth'))
def delegatedtasks(request):
    context = {}
    context['title'] = 'Перепорученные задачи'
    context['privileges'] = request.user.profile.get_plist()
    context['cur_date'] = datetime.now()
    if 'TD' not in context['privileges']:
        return redirect('newtasks')
    try:
        context['tasks'] = Task.objects.filter(target_employee=request.user.profile.employee).exclude(
            delegated_employee=None).select_related('target_employee').order_by('-updated_at')
    except:
        return redirect('home')
    return render(request, 'tasks/delegatedtasks.html', context)
# Действия над задачей


@login_required(login_url=reverse_lazy('auth'))
def task_add(request):
    try:
        employee = request.user.profile.employee
    except:
        return redirect('home')
    context = {}
    context['title'] = 'Новая задача'
    context['privileges'] = request.user.profile.get_plist()
    context['button'] = 'Создать'
    if 'T' not in context['privileges']:
        raise PermissionDenied
    if request.method == 'GET':
        context['form'] = TaskAddForm()
        return render(request, 'tasks/task_add.html', context)
    if request.method == 'POST':
        context['form'] = TaskAddForm(request.POST, request.FILES)
        if context['form'].is_valid():
            Task.objects.create(
                **context['form'].cleaned_data, status='C', created_who=employee)
            return redirect('tasks')
        return render(request, 'tasks/task_add.html', context)


@login_required(login_url=reverse_lazy('auth'))
def task_update(request, pk):
    try:
        employee = request.user.profile.employee
    except:
        return redirect('home')
    context = {}
    context['title'] = 'Редактировать задачу'
    context['privileges'] = request.user.profile.get_plist()
    context['obj'] = get_object_or_404(Task, pk=pk)
    context['button'] = 'Изменить'
    if 'T' not in context['privileges']:
        raise PermissionDenied
    if context['obj'].created_who != employee:
        raise PermissionDenied
    if request.method == 'GET':
        context['form'] = TaskAddForm(instance=context['obj'])
        return render(request, 'tasks/task_add.html', context)
    if request.method == 'POST':
        context['form'] = TaskAddForm(
            request.POST, request.FILES, instance=context['obj'])
        if context['form'].is_valid():
            context['form'].save()
            context['obj'].status = 'C'
            context['obj'].delegated_employee = None
            context['obj'].comments = ''
            context['obj'].answer = ''
            context['obj'].answer_file = None
            context['obj'].save()
            return redirect('tasks')
        return render(request, 'tasks/task_add.html', context)


@login_required(login_url=reverse_lazy('auth'))
def task_delete(request, pk):
    task = get_object_or_404(Task, pk=pk)
    try:
        employee = request.user.profile.employee
    except:
        return redirect('home')
    if task.created_who != employee:
        raise PermissionDenied
    if request.method == 'POST':
        task.delete()
        return redirect(request.META.get('HTTP_REFERER'))


@login_required(login_url=reverse_lazy('auth'))
def task_accept(request, pk):
    task = get_object_or_404(Task, pk=pk)
    can_accept = False
    try:
        employee = request.user.profile.employee
    except:
        return redirect('home')
    if task.target_employee == employee and task.status == 'C':
        can_accept = True
    if task.delegated_employee == employee and task.status == 'D':
        can_accept = True
    if can_accept == False:
        raise Http404('Tasks not found')
    task.status = 'A'
    task.save()
    return redirect('acceptedtasks')


@login_required(login_url=reverse_lazy('auth'))
def task_answer(request, pk):
    context = {}
    try:
        employee = request.user.profile.employee
    except:
        return redirect('home')
    context['title'] = 'Отчет по задаче'
    context['privileges'] = request.user.profile.get_plist()
    context['obj'] = get_object_or_404(Task, pk=pk)
    context['button'] = 'Отчитаться'
    if context['obj'].target_employee != employee and context['obj'].delegated_employee != employee:
        raise Http404('Task not found')
    if context['obj'].delegated_employee and context['obj'].target_employee == employee:
        raise Http404('Task not found')
    if context['obj'].status not in ['A', 'R']:
        raise Http404('Task not found')
    if request.method == 'GET':
        context['form'] = TaskAnswerForm(instance=context['obj'])
        return render(request, 'tasks/task_answer.html', context)
    if request.method == 'POST':
        context['form'] = TaskAnswerForm(
            request.POST, request.FILES, instance=context['obj'])
        if context['form'].is_valid():
            context['form'].save()
            if context['obj'].target_employee == employee:
                context['obj'].status = 'I'
                context['obj'].save()
            else:
                context['obj'].status = 'FI'
                context['obj'].save()
            return redirect('acceptedtasks')
        return render(request, 'tasks/task_answer.html', context)


@login_required(login_url=reverse_lazy('auth'))
def task_to_receive(request, pk):
    if request.method == 'GET':
        raise Http404('Tasks not found')
    task = get_object_or_404(Task, pk=pk)
    can_receive = False
    try:
        employee = request.user.profile.employee
    except:
        return redirect('home')
    if task.created_who == employee and task.status == 'I':
        can_receive = True
    if task.target_employee == employee and task.status == 'FI':
        can_receive = True
    if can_receive == False:
        raise PermissionDenied
    if 'TD' not in request.user.profile.get_plist() and 'T' not in request.user.profile.get_plist():
        raise PermissionDenied
    now = datetime.now()
    task.comments = task.comments + "{}.{}.{}  {}:{}".format(now.day, now.month, now.year, now.hour, now.minute) + ' ' + employee.__str__() + ': ' + \
        request.POST['comments'] + '<br>'
    task.status = 'R'
    task.save()
    return redirect(request.META.get('HTTP_REFERER'))


@login_required(login_url=reverse_lazy('auth'))
def task_solve(request, pk):
    task = get_object_or_404(Task, pk=pk)
    try:
        employee = request.user.profile.employee
    except:
        return redirect('home')
    if task.status == 'FI' and task.target_employee == employee:
        task.status = 'I'
        task.save()
        return redirect('delegatedtasks')
    if task.status == 'I' and task.created_who == employee:
        task.status = 'S'
        task.save()
    return redirect(request.META.get('HTTP_REFERER'))
