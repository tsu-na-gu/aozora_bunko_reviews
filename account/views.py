from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.views import LoginView, LogoutView
from django.http import HttpResponseRedirect
from django.utils.http import url_has_allowed_host_and_scheme
from django.urls import reverse_lazy
from django.views.generic import CreateView, FormView, UpdateView
from django.contrib.auth import login
from account.forms import CustomLoginForm, CustomRegisterForm
from django.contrib import messages

from account.models import Profile


class CustomLoginView(LoginView):
    form_class = CustomLoginForm
    template_name = 'registration/login.html'

    def get_success_url(self):
        next_url = self.request.GET.get('next', '') or self.request.POST.get('next', '')
        if next_url and  url_has_allowed_host_and_scheme(next_url, allowed_hosts={self.request.get_host()}):
            return next_url
        else:
            return reverse_lazy('index')

    def from_invalid(self, form):
        for field, errors in form.errors.items():
            for error in errors:
                messages.error(self.request, error)
        return self.render_to_response(self.get_context_data(form=form))

    def form_valid(self, form):
        messages.success(self.request, 'ログインに成功しました！')
        return super().form_valid(form)


class CustomLogoutView(LogoutView):
    next_page = reverse_lazy('index')

    def dispatch(self, request, *args, **kwargs):
        messages.success(request, 'ログアウトしました')
        return super().dispatch(request, *args, **kwargs)


class CustomRegisterView(FormView):
    template_name = 'registration/register.html'
    form_class = CustomRegisterForm
    success_url = reverse_lazy('profile')

    def form_valid(self, form):
        new_user = form.save(commit=False)
        new_user.set_password(form.cleaned_data['password1'])
        new_user.save()
        Profile.objects.create(user=new_user)
        login(self.request, new_user)
        success_url = reverse_lazy('index') + '?new_user=true'

        return HttpResponseRedirect(success_url)


class ProfileUpdateView(LoginRequiredMixin, UpdateView):
    model = Profile
    fields = []
    template_name = 'profile.html'
    success_url = reverse_lazy('profile')

    def get_object(self):
        return self.request.user.profile

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['show_success_dialog'] = self.request.GET.get('new_user')
        return context
