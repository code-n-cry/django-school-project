from django.urls import path

import homepage.views

app_name = 'homepage'

urlpatterns = [path('', homepage.views.HomeView.as_view(), name='home')]
