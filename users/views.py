import datetime

import django.core.mail
import django.urls
import django.utils.timezone
import django.views.generic
from django.conf import settings
from django.contrib import messages
from django.contrib.auth import get_user_model
from django.contrib.auth.decorators import login_required
from django.shortcuts import redirect
from django.utils.decorators import method_decorator
from django.utils.translation import gettext_lazy
from django.views import View

import tasks.models
import users.forms
import users.models


@method_decorator(login_required, name='dispatch')
class ProfileView(django.views.generic.FormView):
    template_name = 'users/profile.html'
    model = get_user_model()
    form_class = users.forms.ProfileForm
    http_method_names = ['get', 'head', 'post']

    def get(self, request, *args, **kwargs):
        form = self.form_class(instance=request.user)
        extra_context = {'form': form}
        context = self.get_context_data(**kwargs)
        context.update(extra_context)
        return self.render_to_response(context)

    def post(self, request, *args, **kwargs):
        form = self.form_class(
            request.POST, request.FILES, instance=request.user
        )
        if form.is_valid():
            if request.FILES:
                request.user.avatar = request.FILES['avatar']
            form.save()
        extra_context = {'form': form}
        context = self.get_context_data(**kwargs)
        context.update(extra_context)
        return self.render_to_response(context)


@method_decorator(login_required, name='dispatch')
class InvitesView(django.views.generic.ListView):
    context_object_name = 'invites'
    template_name = 'users/invites.html'

    def get_queryset(self):
        return (
            users.models.Invite.objects.filter(to_user=self.request.user.pk)
            .select_related(users.models.Invite.from_team.field.name)
            .only(
                '__'.join([users.models.Invite.from_team.field.name, 'name'])
            )
        )


class InviteBaseDetailView(django.views.generic.DetailView):
    def get_queryset(self):
        return users.models.Invite.objects.filter(
            pk=self.kwargs['pk'], to_user=self.request.user.pk
        )

    def get_object(self):
        obj = self.get_queryset()
        if not obj:
            return None
        return obj


@method_decorator(login_required, name='dispatch')
class InviteAcceptView(InviteBaseDetailView):
    http_method_names = ['get']

    def get(self, *args, **kwargs):
        invite = self.get_object()
        if invite:
            users.models.Member.objects.create(
                user=self.request.user, team=invite.from_team
            )
            invite.delete()
            return redirect('users:invites')
        return redirect('users:invites')


@method_decorator(login_required, name='dispatch')
class InviteRejectView(InviteBaseDetailView):
    http_method_names = ['get']

    def get(self, *args, **kwargs):
        invite = self.get_object()
        if invite:
            invite.delete()
            return redirect('users:invites')
        return redirect('users:invites')


class ActivateNewView(View):
    http_method_names = ['get', 'head']

    def get(self, request, username, *args, **kwargs):
        user = users.models.User.objects.filter(
            username=username,
            date_joined__range=[
                django.utils.timezone.now() - datetime.timedelta(hours=12),
                django.utils.timezone.now(),
            ],
        ).first()
        if not user:
            user = users.models.User.objects.filter(username=username).delete()
            messages.error(
                request,
                gettext_lazy(
                    'Прошло больше 12 часов, ссылка уже не работает:('
                ),
            )
            return redirect('homepage:home')
        user.is_active = True
        user.save()
        messages.success(request, gettext_lazy('Вы активированы!'))
        return redirect('homepage:home')


class ActivateView(View):
    http_method_names = ['get', 'head']

    def get(self, request, username, *args, **kwargs):
        user = users.models.User.objects.filter(
            username=username,
            last_failed_login_date__range=[
                django.utils.timezone.now() - datetime.timedelta(weeks=1),
                django.utils.timezone.now(),
            ],
        ).first()
        if not user:
            user = users.models.User.objects.filter(username=username).delete()
            messages.error(
                request,
                gettext_lazy('Прошла неделя, ссылка уже не работает:('),
            )
            return redirect('homepage:home')
        user.is_active = True
        user.save()
        messages.success(request, 'Аккаунт восстановлен')
        return redirect('auth:login')


class SignUpView(django.views.generic.FormView):
    model = users.models.User
    template_name = 'users/signup.html'
    form_class = users.forms.SignUpForm
    success_url = django.urls.reverse_lazy('auth:login')
    http_method_names = ['get', 'head', 'post']

    def get(self, request, *args, **kwargs):
        if request.user.is_authenticated:
            messages.info(request, gettext_lazy('Вы уже авторизованы!'))
            return redirect('homepage:home')
        return self.render_to_response(self.get_context_data(**kwargs))

    def post(self, request, *args, **kwargs):
        form = self.form_class(request.POST)
        if form.is_valid():
            email_text = ''.join(
                [
                    'Ваша ссылка для активации: ',
                    self.request.build_absolute_uri(
                        django.urls.reverse(
                            'auth:activate_new',
                            kwargs={'username': form.cleaned_data['username']},
                        )
                    ),
                ]
            )
            django.core.mail.send_mail(
                gettext_lazy('Активация'),
                email_text,
                settings.FROM_EMAIL,
                [form.cleaned_data['email']],
                fail_silently=False,
            )
            form.save()
            return redirect(self.success_url)
        context = self.get_context_data()
        context.update(form=form)
        return self.render_to_response(context, **kwargs)


class UserListView(django.views.generic.ListView):
    template_name = 'users/list.html'
    queryset = users.models.User.objects.public()
    paginate_by = 5
    context_object_name = 'users'
    http_method_names = ['get', 'head']


class UserDetailView(django.views.generic.DetailView):
    template_name = 'users/detail.html'
    queryset = users.models.User.objects.public()
    context_object_name = 'user'
    comment_form = users.forms.CommentForm
    http_method_names = ['get', 'head', 'post']

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        users_comments = (
            users.models.Comment.objects.filter(
                to_user=self.get_object(), is_reported=False
            )
            .select_related(users.models.Comment.author.field.name)
            .values(
                users.models.Comment.content.field.name,
                users.models.Comment.id.field.name,
                '__'.join(
                    [
                        users.models.Comment.author.field.name,
                        users.models.User.username.field.name,
                    ]
                ),
            )
        )
        users_tasks = tasks.models.Task.objects.filter(
            users=self.request.user, completed_date__isnull=False
        )
        if self.request.user.is_authenticated:
            context.update(form=self.comment_form())
        context.update(all_tasks_count=users_tasks, comments=users_comments)
        return context

    def post(self, request, *args, **kwargs):
        if request.user.is_authenticated:
            form = self.comment_form(request.POST)
            if form.is_valid():
                comment = form.save(commit=False)
                comment.author = request.user
                comment.to_user = self.get_object()
                comment.save()
        return redirect(
            django.urls.reverse(
                'users:user_detail', kwargs={'pk': self.get_object().pk}
            )
        )


class UnauthorizedView(django.views.generic.TemplateView):
    template_name = None
    http_method_names = ['get', 'head']


@method_decorator(login_required, name='dispatch')
class SendRequestView(django.views.generic.FormView):
    template_name = 'users/request_form.html'
    success_url = '/'
    form_class = users.forms.RequestForm

    def post(self, request, *args, **kwargs):
        form = self.form_class(request.POST)
        if form.is_valid():
            team_request = users.models.Request.objects.create(
                from_user=request.user, to_team=form.cleaned_data['to_team']
            )
            team_request.save()
        return super().post(request, *args, **kwargs)

    def form_valid(self, form):
        if form.is_valid():
            team = form.cleaned_data['to_team']
            if self.request.user in team.members.all():
                form.add_error(
                    'to_team',
                    gettext_lazy('Вы уже состоите в этой команде!'),
                )
                return super().form_invalid(form)
        return super().form_valid(form)


class CommentReportView(django.views.generic.DetailView):
    http_method_names = ['get']

    def get_queryset(self):
        return users.models.Comment.objects.filter(
            pk=self.kwargs['pk']
        ).first()

    def get_object(self):
        obj = self.get_queryset()
        if not obj:
            return None
        return obj

    def get(self, *args, **kwargs):
        comment = self.get_object()
        if comment:
            comment.is_reported = True
            comment.save()
            return redirect('homepage:home')
        return redirect('homepage:home')
