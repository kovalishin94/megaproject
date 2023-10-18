from django.db import models
from staff.models import Employee


class Test(models.Model):
    title = models.CharField(
        max_length=200, unique=True, verbose_name='Название')
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='Создан')

    def __str__(self):
        return self.title

    class Meta:
        verbose_name = 'Тест'
        verbose_name_plural = 'Тесты'


class Question(models.Model):
    title = models.CharField(max_length=500, verbose_name='Вопрос')
    test = models.ForeignKey(
        Test, on_delete=models.CASCADE, verbose_name='Тест')
    order_number = models.PositiveSmallIntegerField(
        verbose_name='Порядковый номер')

    def __str__(self):
        return self.title

    class Meta:
        verbose_name = 'Вопрос'
        verbose_name_plural = 'Вопросы'
        unique_together = ('test', 'order_number')


class Choice(models.Model):
    title = models.CharField(max_length=200, verbose_name='Ответ')
    question = models.ForeignKey(Question, on_delete=models.CASCADE)
    order_number = models.PositiveSmallIntegerField(
        verbose_name='Порядковый номер')
    is_correct = models.BooleanField(
        verbose_name='Правильный/Неправильный', default=False)

    def __str__(self):
        return self.title

    class Meta:
        verbose_name = 'Вариант ответа'
        verbose_name_plural = 'Варианты ответов'
        unique_together = ('question', 'order_number')


class Vote(models.Model):
    employee = models.ForeignKey(
        Employee, on_delete=models.CASCADE, verbose_name='Сотрудник')
    question = models.ForeignKey(
        Question, on_delete=models.CASCADE, verbose_name='Вопрос')
    choice = models.ForeignKey(
        Choice, on_delete=models.CASCADE, verbose_name='Выбранный вариант')

    class Meta:
        verbose_name = 'Выбранный вариант ответа'
        verbose_name_plural = 'Выбранные варианты ответов'


class Result(models.Model):
    employee = models.ForeignKey(
        Employee, on_delete=models.CASCADE, verbose_name='Сотрудник')
    test = models.ForeignKey(
        Test, on_delete=models.CASCADE, verbose_name='Тест')
    count_right = models.SmallIntegerField(
        default=0, blank=True, verbose_name='Количество верных ответов')
    count_false = models.SmallIntegerField(
        default=0, blank=True, verbose_name='Количество неверных ответов')
    description = models.TextField(blank=True, verbose_name='Описание')

    class Meta:
        verbose_name = 'Результат'
        verbose_name_plural = 'Результаты'
