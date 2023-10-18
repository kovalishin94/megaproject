from django.contrib import admin
from django.conf import settings
from django.urls import path, include, re_path
from django.views.static import serve
from django.conf.urls import handler403

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('core.urls')),
    path('users/', include('userprofiles.urls')),
    path('staff/', include('staff.urls')),
    path('tasks/', include('tasks.urls')),
    path('tests/', include('testing.urls')),
]

handler403 = 'core.views.forbidden_403'

if settings.DEBUG:
    urlpatterns += [
        re_path(r'^media/(?P<path>.*)$', serve, {
            'document_root': settings.MEDIA_ROOT,
        }),
        path('__debug__/', include('debug_toolbar.urls')),
    ]
