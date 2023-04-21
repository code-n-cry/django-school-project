from django.urls import path

import skills.views

app_name = 'skills'

urlpatterns = [
    path('', skills.views.ListSkillView.as_view(), name='list'),
    path('create/', skills.views.AddSkillView.as_view(), name='create'),
]
