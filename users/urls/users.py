import django.contrib.auth.views
import django.urls

import users.views

app_name = 'users'

urlpatterns = [
    django.urls.path(
        '',
        users.views.UserListView.as_view(),
        name='user_list',
    ),
    django.urls.path(
        '<int:pk>/',
        users.views.UserDetailView.as_view(),
        name='user_detail',
    ),
    django.urls.path(
        'me/',
        users.views.ProfileView.as_view(),
        name='profile',
    ),
    django.urls.path(
        'invites/',
        users.views.InvitesView.as_view(),
        name='invites',
    ),
    django.urls.path(
        'invites/<int:pk>/yes',
        users.views.InviteAcceptView.as_view(),
        name='invite_accept',
    ),
    django.urls.path(
        'invites/<int:pk>/no',
        users.views.InviteRejectView.as_view(),
        name='invite_reject',
    ),
    django.urls.path(
        'requests/send/',
        users.views.SendRequestView.as_view(),
        name='send_request',
    ),
]
