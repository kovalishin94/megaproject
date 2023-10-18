from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.urls import reverse_lazy
from django.core.exceptions import PermissionDenied
from .forms import UserCreationForm, PrivilegeChooseForm, UserUpdateForm
from .models import Userprofile, Privilege
from django.contrib.auth.models import User


def authentication(request):
    if request.user.is_authenticated:
        return redirect('home')
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect('home')
        else:
            messages.error(request, 'Неверный логин или пароль')
            return redirect('auth')
    return render(request, template_name='userprofiles/auth.html')


@login_required(login_url=reverse_lazy('auth'))
def logout_view(request):
    logout(request)
    return redirect('auth')


@login_required(login_url=reverse_lazy('auth'))
def user_create(request):
    context = {}
    context['privileges'] = request.user.profile.get_plist()
    context['title'] = 'Создать пользователя'

    if 'AD' not in context['privileges']:
        raise PermissionDenied

    if request.method == 'GET':
        context['form'] = UserCreationForm()
        context['form2'] = PrivilegeChooseForm()

    if request.method == 'POST':
        context['form'] = UserCreationForm(request.POST)
        context['form2'] = PrivilegeChooseForm(request.POST)
        if context['form'].is_valid() and context['form2'].is_valid():
            new_user = User.objects.create_user(
                context['form'].cleaned_data['username'], password=context['form'].cleaned_data['password1'])
            new_profile = Userprofile.objects.create(user=new_user)
            admincheck = False
            for i in context['form2'].cleaned_data['privileges']:
                if 'AD' == i.title:
                    admincheck = True
                    break
            if admincheck:
                new_profile.privileges.set(Privilege.objects.all())
            else:
                new_profile.privileges.set(
                    context['form2'].cleaned_data['privileges'])
            new_profile.save()
            return redirect('users')
    return render(request, 'userprofiles/user_create.html', context)


@login_required(login_url=reverse_lazy('auth'))
def user_update(request, pk):
    context = {}
    context['privileges'] = request.user.profile.get_plist()
    context['title'] = 'Редактировать пользователя'
    userprofile = get_object_or_404(Userprofile, pk=pk)
    user = get_object_or_404(User, pk=userprofile.user.pk)

    if user.username == 'admin':
        raise PermissionDenied

    if 'AD' not in context['privileges']:
        raise PermissionDenied

    if request.method == 'GET':
        context['form'] = UserUpdateForm(initial={'username': user.username})
        context['form2'] = PrivilegeChooseForm(instance=userprofile)

    if request.method == 'POST':
        context['form'] = UserUpdateForm(request.POST)
        context['form2'] = PrivilegeChooseForm(
            request.POST, instance=userprofile)
        if context['form'].is_valid() and context['form2'].is_valid():
            user.username = context['form'].cleaned_data['username']
            user.set_password(context['form'].cleaned_data['password1'])
            user.save()
            admincheck = False
            for i in context['form2'].cleaned_data['privileges']:
                if 'AD' == i.title:
                    admincheck = True
                    break
            if admincheck:
                userprofile.privileges.set(Privilege.objects.all())
            else:
                userprofile.privileges.set(
                    context['form2'].cleaned_data['privileges'])
            userprofile.save()
            return redirect('users')
    return render(request, 'userprofiles/user_update.html', context)


@login_required(login_url=reverse_lazy('auth'))
def users(request):
    context = {}
    context['privileges'] = request.user.profile.get_plist()
    context['title'] = 'Список пользователей'

    if 'AD' not in context['privileges']:
        raise PermissionDenied

    context['userprofiles'] = Userprofile.objects.prefetch_related(
        'privileges', 'user', 'employee')

    return render(request, 'userprofiles/users.html', context)


@login_required(login_url=reverse_lazy('auth'))
def user_delete(request, pk):
    context = {}
    context['privileges'] = request.user.profile.get_plist()
    if 'AD' not in context['privileges']:
        raise PermissionDenied
    if request.method == 'GET':
        return redirect(request.META.get('HTTP_REFERER'))
    if request.method == 'POST':
        user = get_object_or_404(User, pk=pk)
        if user.username == 'admin':
            raise PermissionDenied
        user.delete()
        return redirect(request.META.get('HTTP_REFERER'))
