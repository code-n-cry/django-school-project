from django.urls import path

import homepage.views

app_name = 'home'

urlpatterns = [path('', homepage.views.home, name='home')]
