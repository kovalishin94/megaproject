from django.urls import reverse_lazy
from .models import Employee, Department
from .forms import EmployeeForm
from django.shortcuts import render, redirect, get_object_or_404
from django.http import Http404, HttpResponse
from django.core.exceptions import PermissionDenied
from django.contrib.auth.decorators import login_required
import xlwt

# Вывод таблицей всех сотрудников


@login_required(login_url=reverse_lazy('auth'))
def staff(request):
    context = {}
    context['privileges'] = request.user.profile.get_plist()

    if 'S' not in context['privileges']:
        raise PermissionDenied

    context['title'] = 'Сотрудники'
    context['employees'] = Employee.objects.select_related('department')
    context['departments'] = Department.objects.all().order_by('title')
    return render(request, 'staff/staff.html', context)

# Добавление нового сотрудника


@login_required(login_url=reverse_lazy('auth'))
def employee_add(request):
    context = {}
    context['privileges'] = request.user.profile.get_plist()

    if 'S' not in context['privileges']:
        raise PermissionDenied

    context['title'] = 'Новый сотрудник'
    context['button'] = 'Добавить'

    if request.method == "GET":
        context['form'] = EmployeeForm()
        return render(request, 'staff/staff_add.html', context)

    if request.method == 'POST':
        context['form'] = EmployeeForm(request.POST, request.FILES)
        if context['form'].is_valid():
            # context['form'].save()
            Employee.objects.create(**context['form'].cleaned_data)
            return redirect('staff')
        return render(request, 'staff/staff_add.html', context)

# Редактирование сотрудника


@login_required(login_url=reverse_lazy('auth'))
def employee_update(request, pk):
    context = {}
    context['privileges'] = request.user.profile.get_plist()

    if 'S' not in context['privileges']:
        raise PermissionDenied

    context['title'] = 'Редактирование сотрудника'
    context['button'] = 'Изменить'
    context['obj'] = get_object_or_404(Employee, pk=pk)
    if request.method == 'GET':
        context['form'] = EmployeeForm(instance=context['obj'])
        return render(request, 'staff/staff_add.html', context)

    if request.method == 'POST':
        context['form'] = EmployeeForm(
            request.POST, request.FILES, instance=context['obj'])
        if context['form'].is_valid():
            context['form'].save()
            if context['form'].cleaned_data['profile']:
                context['obj'].profile = context['form'].cleaned_data['profile']
                context['obj'].save(update_fields=['profile'])
            return redirect('staff')

    return render(request, 'staff/staff_add.html', context)

# Удаление сотрудника


@login_required(login_url=reverse_lazy('auth'))
def employee_delete(request, pk):

    if request.method == "GET":
        return redirect('staff')

    if 'SD' not in request.user.profile.get_plist():
        raise PermissionDenied

    employee = get_object_or_404(Employee, pk=pk)
    employee.delete()
    return redirect('staff')

# Отвязка профиля


@login_required(login_url=reverse_lazy('auth'))
def untie_profile(request, pk):
    if 'AD' not in request.user.profile.get_plist():
        raise PermissionDenied

    if request.method == 'POST':
        employee = get_object_or_404(Employee, pk=pk)
        if employee.profile.user.username == 'admin':
            raise PermissionDenied
        employee.profile = None
        employee.save(update_fields=['profile'])
        return redirect(request.META.get('HTTP_REFERER'))
    else:
        raise Http404('Not found')

# Вывод всех сотрудников в excel


@login_required(login_url=reverse_lazy('auth'))
def staff_to_excel(request):
    if 'S' not in request.user.profile.get_plist():
        raise PermissionDenied

    response = HttpResponse(content_type='application/ms-excel')
    response['Content-Disposition'] = 'attachment; filename="staff.xlsx"'

    wb = xlwt.Workbook(encoding='utf-8')
    ws = wb.add_sheet('Сотрудники')

    row_num = 0

    font_style = xlwt.XFStyle()
    font_style.font.bold = True

    columns = ['Фамилия', 'Имя', 'Отчество', 'Дата рождения',
               'E-mail', 'Отдел', 'Должность', 'Дата заключения договора', ]

    for col_num in range(len(columns)):
        ws.write(row_num, col_num, columns[col_num], font_style)

    font_style = xlwt.XFStyle()

    rows = Employee.objects.all().values_list('last_name', 'first_name', 'surname',
                                              'date_of_birth', 'email', 'department', 'position', 'agreement_date')
    for row in rows:
        row_num += 1
        for col_num in range(len(row)):
            ws.write(row_num, col_num, row[col_num], font_style)

    wb.save(response)
    return response


@login_required(login_url=reverse_lazy('auth'))
def department_add(request):
    if request.method == 'GET':
        return redirect(request.META.get('HTTP_REFERER'))
    if 'S' not in request.user.profile.get_plist():
        raise PermissionDenied
    if request.POST['department_add']:
        Department.objects.create(title=request.POST['department_add'])
    return redirect(request.META.get('HTTP_REFERER'))


@login_required(login_url=reverse_lazy('auth'))
def department_update(request, pk):
    if request.method == 'GET':
        return redirect(request.META.get('HTTP_REFERER'))
    if 'S' not in request.user.profile.get_plist():
        raise PermissionDenied
    department = get_object_or_404(Department, pk=pk)
    if request.POST['department']:
        department.title = request.POST['department']
        department.save()
    return redirect(request.META.get('HTTP_REFERER'))


@login_required(login_url=reverse_lazy('auth'))
def department_delete(request, pk):
    if request.method == 'GET':
        return redirect(request.META.get('HTTP_REFERER'))
    if 'S' not in request.user.profile.get_plist():
        raise PermissionDenied
    department = get_object_or_404(Department, pk=pk)
    department.delete()
    return redirect(request.META.get('HTTP_REFERER'))
