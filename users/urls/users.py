from django.urls import path

from users import views

app_name = 'users'

urlpatterns = [
    path('profile/', views.ProfileView.as_view(), name='profile'),
]
