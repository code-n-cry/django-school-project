from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import include, path, re_path
from django.views.static import serve

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('homepage.urls')),
    path('auth/', include('users.urls.auth')),
    path('users/', include('users.urls.users')),
    path('auth/', include('django.contrib.auth.urls')),
    path('meetings/', include('tasks.urls.meetings')),
    path('skills/', include('skills.urls')),
    path('tasks/', include('tasks.urls.tasks')),
    path('teams/', include('teams.urls')),
    path('i18n/', include('django.conf.urls.i18n')),
    re_path(
        r'^media/(?P<path>.*)$', serve, {'document_root': settings.MEDIA_ROOT}
    ),
    re_path(
        r'^static/(?P<path>.*)$',
        serve,
        {'document_root': settings.STATIC_ROOT},
    ),
]

if settings.DEBUG:
    import debug_toolbar

    urlpatterns += (path('__debug__/', include(debug_toolbar.urls)),)
    urlpatterns += static(
        settings.MEDIA_URL, document_root=settings.MEDIA_ROOT
    )
