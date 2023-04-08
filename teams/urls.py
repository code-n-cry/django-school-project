from django.urls import path

from teams.views import CreateTeamView

app_name = 'teams'

urlpatterns = [
    path('create/', CreateTeamView.as_view(), name='create'),
]
