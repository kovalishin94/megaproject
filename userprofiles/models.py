from django.db import models
from django.utils import timezone
from django.core.cache import cache
from django.contrib.auth.models import User


class Privilege(models.Model):
    title = models.CharField(max_length=2, verbose_name='Привигегия')
    description = models.CharField(
        max_length=200, verbose_name='Описание', blank=True)

    def __str__(self) -> str:
        return str(self.description)

    class Meta:
        verbose_name = 'Привилегия'
        verbose_name_plural = 'Привилегии'


class Userprofile(models.Model):
    user = models.OneToOneField(
        User, on_delete=models.CASCADE, related_name='profile', verbose_name='Пользователь')
    privileges = models.ManyToManyField(
        Privilege, related_name='privilege', blank=True, verbose_name='Привилегии')

    def __str__(self) -> str:
        return str(self.user)

    def get_plist(self):
        result = []
        for i in self.privileges.all():
            result.append(i.title)
        return result

    def is_online(self):
        last_seen = cache.get(f'last-seen-{self.user.id}')
        if last_seen is not None and timezone.now() < last_seen + timezone.timedelta(seconds=300):
            return True
        return False

    class Meta:
        verbose_name = 'Профиль'
        verbose_name_plural = 'Профили'
