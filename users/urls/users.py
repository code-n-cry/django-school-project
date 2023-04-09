import django.urls

import users.views

app_name = 'users'

urlpatterns = [
    django.urls.path(
        'detail/<int:pk>/',
        users.views.UserDetailView.as_view(),
        name='user_detail',
    ),
    django.urls.path(
        'profile/', users.views.ProfileView.as_view(), name='profile'
    ),
]
