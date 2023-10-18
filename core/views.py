from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.urls import reverse_lazy
from django.http import Http404, JsonResponse
from tasks.models import Task
from django.db.models import Q
from datetime import date


@login_required(login_url=reverse_lazy('auth'))
def index(request):
    context = {}
    context['privileges'] = request.user.profile.get_plist()
    return render(request, 'core/index.html', context)


@login_required(login_url=reverse_lazy('auth'))
def get_tasks_count(request):
    try:
        employee = request.user.profile.employee
    except:
        raise Http404('Not found employee')
    context = {}
    context['solved'] = Task.objects.filter(status='S').count()
    context['notaccepted'] = Task.objects.filter(
        Q(status='C') | Q(status='D')).count()
    context['overdue'] = Task.objects.exclude(
        status='S').filter(deadline__lt=date.today()).count()
    context['accepted'] = Task.objects.filter(
        Q(deadline__gt=date.today()), Q(status='A') | Q(status='R')).count()
    context['inspect'] = Task.objects.filter(
        Q(status='I') | Q(status='FI')).count()
    return JsonResponse(context)


def forbidden_403(request, exception):
    response = render(request, 'core/403.html')
    response.status_code = 403
    return response
