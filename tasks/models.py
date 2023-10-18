from django.db import models
from staff.models import Employee
from datetime import date, timedelta
import os
from django.core.exceptions import ValidationError


def validate_date(value):
    if value <= date.today():
        raise ValidationError(
            ('Дата не может быть меньше текущей'),
            params={'value': value},
        )


class Task(models.Model):
    STATUS = [
        ('C', 'Поручена'),
        ('D', 'Перепоручена'),
        ('A', 'В работе'),
        ('I', 'На проверке'),
        ('FI', 'Первичная проверка'),
        ('R', 'На доработке'),
        ('S', 'Выполнена'),
    ]

    # Варианты жизненных циклов задачи:
    # C - A - I - S
    # C - A - I - R - I - S
    # C - D - A - FI- I - S
    # C - D - A - FI - R - FI - I - R - FI - I - S

    title = models.CharField(max_length=100, verbose_name='Заголовок')
    description = models.TextField(blank=True, verbose_name='Описание')
    deadline = models.DateField(default=date.today(
    )+timedelta(days=1), verbose_name='Контрольный срок', validators=[validate_date])
    created_at = models.DateTimeField(
        auto_now_add=True, verbose_name='Дата создания')
    created_who = models.ForeignKey(
        Employee, on_delete=models.SET_NULL, null=True, related_name='created_who', verbose_name='Создана', editable=False)
    target_employee = models.ForeignKey(
        Employee, on_delete=models.SET_NULL, null=True, related_name='target', verbose_name='Назначена на')
    delegated_employee = models.ForeignKey(
        Employee, on_delete=models.SET_NULL, null=True, related_name='delegated', verbose_name='Делегировано')
    task_file = models.FileField(
        blank=True, upload_to='tasks/%Y/%m/%d/', null=True, verbose_name='Файл прилагаемый к задаче')
    answer = models.TextField(blank=True, verbose_name='Отчет')
    answer_file = models.FileField(
        blank=True, upload_to='answers/%Y/%m/%d/', null=True, verbose_name='Файл прилагаемый к отчету')
    updated_at = models.DateTimeField(
        auto_now=True, verbose_name='Дата изменения')
    status = models.CharField(
        max_length=12, choices=STATUS, verbose_name='Статус', default='C', editable=False)
    comments = models.TextField(blank=True, verbose_name='Комментарий')

    class Meta:
        verbose_name = 'Задача'
        verbose_name_plural = 'Задачи'

    def __str__(self):
        return self.title

    def tfilename(self):
        return os.path.basename(self.task_file.name)

    def afilename(self):
        return os.path.basename(self.answer_file.name)
