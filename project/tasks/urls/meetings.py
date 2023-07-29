import django.contrib.auth.views
import django.urls

import tasks.views

app_name = 'meetings'

urlpatterns = [
    django.urls.path(
        '<int:pk>/detail/',
        tasks.views.MeetingDetailView.as_view(),
        name='detail',
    ),
    django.urls.path(
        'yours/',
        tasks.views.YourMeetingsView.as_view(),
        name='yours',
    ),
]
