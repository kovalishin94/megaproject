from django.db import models
from django.urls import reverse
from userprofiles.models import Userprofile


class Department(models.Model):
    title = models.CharField(
        max_length=200, verbose_name="Наименование отдела")

    def __str__(self):
        return self.title

    class Meta:
        verbose_name = 'Отдел'
        verbose_name_plural = 'Отделы'


class Employee(models.Model):
    first_name = models.CharField(max_length=30, verbose_name='Имя')
    last_name = models.CharField(max_length=50, verbose_name='Фамилия')
    surname = models.CharField(
        max_length=50, blank=True, verbose_name='Отчество')
    date_of_birth = models.DateField(
        blank=True, verbose_name='Дата рождения', null=True)
    email = models.EmailField(blank=True, max_length=30, verbose_name='E-mail')
    photo = models.ImageField(
        blank=True, upload_to='photos/%Y/%m/%d/', verbose_name='Фото', null=True)
    department = models.ForeignKey(
        Department, on_delete=models.SET_NULL, null=True, verbose_name='Отдел', blank=True)
    position = models.CharField(
        max_length=200, blank=True, verbose_name='Должность')
    agreement_date = models.DateField(
        blank=True, verbose_name='Дата заключения трудового договора', null=True)
    created_at = models.DateTimeField(
        auto_now_add=True, verbose_name='Дата и время создания карточки работника')
    updated_at = models.DateTimeField(
        auto_now=True, verbose_name='Дата и время последних изменений')
    profile = models.OneToOneField(Userprofile, blank=True, null=True,
                                   on_delete=models.PROTECT, verbose_name='Профиль', related_name='employee')
    test_results = models.TextField(
        blank=True, verbose_name='Результаты тестов')

    def __str__(self) -> str:
        return self.last_name + ' ' + self.first_name + ' ' + self.surname

    def count_filling(self):
        count = 2
        if self.surname:
            count += 1
        if self.date_of_birth:
            count += 1
        if self.email:
            count += 1
        if self.photo:
            count += 1
        if self.agreement_date:
            count += 1
        if self.position:
            count += 1
        return count/8*100

    class Meta:
        verbose_name = 'Работник'
        verbose_name_plural = 'Работники'
        ordering = ['created_at']
