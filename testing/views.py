from django.shortcuts import render, redirect, get_object_or_404
from django.http import Http404
from django.urls import reverse_lazy
from django.contrib.auth.decorators import login_required
from django.core.exceptions import PermissionDenied
from .models import Test, Question, Choice, Vote, Result
from .forms import AddTestForm
from django.core.paginator import Paginator
from datetime import datetime


def check_permission(request):
    context = {}
    context['privileges'] = request.user.profile.get_plist()
    try:
        request.user.profile.employee
    except:
        return redirect('home')
    if 'TE' not in context['privileges']:
        raise PermissionDenied
    return context


@login_required(login_url=reverse_lazy('auth'))
def tests(request):
    try:
        request.user.profile.employee
    except:
        return redirect('home')
    context = {}
    context['privileges'] = request.user.profile.get_plist()
    context['title'] = 'Тесты'
    context['tests'] = Test.objects.all()
    context['form'] = AddTestForm()
    if request.method == 'POST':
        context['form'] = AddTestForm(request.POST)
        if context['form'].is_valid():
            context['form'].save()
            return redirect('tests')
    return render(request, 'testing/tests.html', context)


@login_required(login_url=reverse_lazy('auth'))
def delete_test(request, pk):
    if request.method == 'GET':
        raise Http404('Тест не найден')
    if request.method == 'POST':
        context = check_permission(request)
        context['test'] = get_object_or_404(Test, pk=pk)
        context['test'].delete()
        return redirect('tests')


@login_required(login_url=reverse_lazy('auth'))
def update_test(request, pk):
    if request.method == 'GET':
        raise Http404('Тест не найден')
    if request.method == 'POST':
        context = check_permission(request)
        context['test'] = get_object_or_404(Test, pk=pk)
        context['form'] = AddTestForm(request.POST, instance=context['test'])
        if context['form'].is_valid():
            context['form'].save()
        return redirect('tests')


@login_required(login_url=reverse_lazy('auth'))
def edit_test(request, pk):
    context = check_permission(request)
    context['test'] = get_object_or_404(Test, pk=pk)
    questions = Question.objects.filter(
        test=context['test']).prefetch_related('choice_set')
    if request.method == 'GET':
        context['title'] = f"Тесты | {context['test'].title}"
        paginator = Paginator(questions, 5)
        page_number = request.GET.get('page')
        context['questions'] = paginator.get_page(page_number)
    if request.method == 'POST':
        Question.objects.create(
            title=request.POST['title'], order_number=questions.count()+1, test=context['test'])
        return redirect(request.META.get('HTTP_REFERER'))
    return render(request, 'testing/edit_test.html', context)


@login_required(login_url=reverse_lazy('auth'))
def delete_question(request, pk):
    if request.method == 'GET':
        raise Http404('Вопрос не найден')
    if request.method == 'POST':
        context = check_permission(request)
        question = get_object_or_404(Question, pk=pk)
        test = question.test
        question.delete()
        count = 1
        for i in Question.objects.filter(test=test):
            i.order_number = count
            i.save()
            count += 1
        return redirect(request.META.get('HTTP_REFERER'))


@login_required(login_url=reverse_lazy('auth'))
def update_question(request, pk):
    if request.method == 'GET':
        raise Http404('Тест не найден')
    if request.method == 'POST':
        context = check_permission(request)
        question = get_object_or_404(Question, pk=pk)
        question.title = request.POST['title']
        question.save()
        return redirect('edit_test', question.test.pk)


@login_required(login_url=reverse_lazy('auth'))
def add_choice(request, pk):
    context = check_permission(request)
    if request.method == 'POST':
        question = get_object_or_404(Question, pk=pk)
        is_correct = False
        if request.POST.get('is_correct'):
            is_correct = True
        choice = question.choice_set.create(
            title=request.POST['choice_title'], order_number=question.choice_set.count()+1, is_correct=is_correct)
        return redirect(request.META.get('HTTP_REFERER'))
    else:
        raise Http404('Not found')


@login_required(login_url=reverse_lazy('auth'))
def delete_choice(request, pk):
    if request.method == 'GET':
        raise Http404('Ответ не найден')
    if request.method == 'POST':
        context = check_permission(request)
        choice = get_object_or_404(Choice, pk=pk)
        question = choice.question
        choice.delete()
        count = 1
        for i in Choice.objects.filter(question=question):
            i.order_number = count
            i.save()
            count += 1
        return redirect(request.META.get('HTTP_REFERER'))


@login_required(login_url=reverse_lazy('auth'))
def solve_test(request, pk):
    try:
        employee = request.user.profile.employee
    except:
        return redirect('home')
    context = {}
    context['privileges'] = request.user.profile.get_plist()
    context['test'] = get_object_or_404(Test, pk=pk)
    context['questions'] = Question.objects.filter(
        test=context['test']).prefetch_related('choice_set')
    context['title'] = f'Тест {context["test"].title}'
    if request.method == 'GET':
        if Result.objects.filter(employee=employee, test=context['test']):
            result = Result.objects.get(
                employee=employee, test=context['test'])
            return redirect('result_test', result.pk)
        if not context['questions']:
            context['error'] = 'Данный тест не доделан: нет вопросов'
            return render(request, 'testing/error_test.html', context)
        for i in context['questions']:
            if not i.choice_set.all():
                context['error'] = 'Данный тест не доделан: нет ответов на некоторые вопросы'
                return render(request, 'testing/error_test.html', context)
    if request.method == 'POST':
        count_right = 0
        count_all = 0
        for i in context['questions']:
            vote = Vote.objects.create(employee=employee,
                                       question=i, choice_id=request.POST.get(f'question{i.pk}'))
            count_all += 1
            if vote.choice.is_correct:
                count_right += 1
        result = Result.objects.create(employee=employee,
                                       test=context['test'], count_right=count_right, count_false=count_all-count_right)
        result.description = f'Тест пройден c результатом {round(count_right*100/count_all, 1)} %'
        result.save()
        now = datetime.now()
        employee.test_results = employee.test_results + "{}.{}.{}  {}:{}".format(
            now.day, now.month, now.year, now.hour, now.minute) + ' ' + f'Пройден тест "{context["test"].title}"' + ' - ' + f'результат {round(count_right*100/count_all, 1)} %' + '<br>'
        employee.save()
        return redirect('result_test', result.pk)
    return render(request, 'testing/solve_test.html', context)


@login_required(login_url=reverse_lazy('auth'))
def result_test(request, pk):
    try:
        employee = request.user.profile.employee
    except:
        return redirect('home')
    context = {}
    context['privileges'] = request.user.profile.get_plist()
    context['result'] = get_object_or_404(Result, pk=pk)
    context['title'] = f'Результаты теста | {context["result"].test.title}'
    if employee != context['result'].employee:
        raise PermissionDenied
    return render(request, 'testing/resulttest.html', context)


@login_required(login_url=reverse_lazy('auth'))
def all_test_results(request, pk):
    context = check_permission(request)
    test = get_object_or_404(Test, pk=pk)
    context['test_title'] = test.title
    context['title'] = f'Спсиок результатов теста {test}'
    context['results'] = test.result_set.all()
    return render(request, 'testing/allresults.html', context)
