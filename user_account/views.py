import html

from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.models import User
from allauth.account.views import LogoutView, SignupView, LoginView, ConfirmEmailView
from django.http import HttpResponseRedirect
from django.shortcuts import redirect
from django.utils.http import url_has_allowed_host_and_scheme, urlencode
from django.urls import reverse_lazy
from django.views.generic import CreateView, FormView, UpdateView, ListView, DetailView
from django.contrib.auth import login
from user_account.forms import CustomLoginForm, CustomSignupForm
from django.contrib import messages
from urllib.parse import parse_qs, unquote, urlparse
from django.urls import reverse
from user_account.models import Profile

class CustomLoginView(LoginView):
    form_class = CustomLoginForm
    template_name = 'account/login.html'

    def get_success_url(self):
        next_url = self.request.GET.get('next', '') or self.request.POST.get('next', '')
        if next_url and url_has_allowed_host_and_scheme(next_url, allowed_hosts={self.request.get_host()}):
            return next_url
        else:
            return reverse_lazy('index')

    def form_invalid(self, form):
        return self.render_to_response(self.get_context_data(form=form))

    def form_valid(self, form):
        return super().form_valid(form)


class CustomLogoutView(LogoutView):
    next_page = reverse_lazy('index')

    def dispatch(self, request, *args, **kwargs):
        return super().dispatch(request, *args, **kwargs)


class CustomSignupView(SignupView):
    template_name = 'account/register.html'
    form_class = CustomSignupForm

    def form_valid(self, form):
        response = super().form_valid(form)
        return response


class ProfileView(LoginRequiredMixin, ListView):
    model = Profile
    template_name = 'profile.html'
    context_object_name = 'user'

    def get_queryset(self):
        return Profile.objects.filter(user=self.request.user)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        user = self.request.user
        search_history = user.search_history.all().order_by('-searched_at')
        for history in search_history:
            decoded_search_term = html.unescape(history.search_term)
            query_params = parse_qs(decoded_search_term)
            values = []
            detail_search = False
            for key, value in query_params.items():
                if key == 'is_children_book':
                    values.append('児童書')
                elif key == 'q' and value[0] == 'detail_search':
                   detail_search = True
                else:
                    values.append(value[0])
            if len(values) > 1:
                history.decoded_search_term = ", ".join(values)
            else:
                history.decoded_search_term = values[0] if values else None

            encoded_params = urlencode(query_params, doseq=True)
            if detail_search:
                history.search_url = f"/detail_search_results/?{encoded_params}"
            else:
                history.search_url = f"/search/?{encoded_params}"

        context['search_history'] = search_history

        review_history = user.review_history.all().order_by('-reviewed_at')

        context['review_history'] = review_history

        context['user'] = user

        return context


class CustomConfirmEmailView(ConfirmEmailView):
    def get(self, *args, **kwargs):
        confirmation = self.get_object()
        confirmation.confirm(self.request)
        messages.success(self.request, 'アカウントの認証に成功しました。ログインして下さい。')
        user = confirmation.email_address.user

        Profile.objects.get_or_create(user=user)

        return redirect(reverse('account_login'))