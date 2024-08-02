from django.urls import path
from user_account.views import CustomLogoutView, CustomSignupView, ProfileView, CustomLoginView, CustomConfirmEmailView
from allauth.account.views import confirm_email, PasswordResetFromKeyDoneView, PasswordResetFromKeyView, \
    PasswordResetDoneView, PasswordResetView, EmailVerificationSentView
from django.contrib.auth import views as auth_views

urlpatterns = [
    # path('login/', CustomLoginView.as_view(), name='account_login'),
    # path('logout/', CustomLogoutView.as_view(), name='account_logout'),
    # path('signup/', CustomSignupView.as_view(), name='account_signup'),
    path('profile/', ProfileView.as_view(), name='profile'),
    # path('confirm-email/', confirm_email, name='account_confirm_email'),
    #
    # path('varify-email/<str:key>/', CustomConfirmEmailView.as_view(), name='account_confirm_email'),
    #
    # path('password-reset/', PasswordResetView.as_view(), name='account_reset_password'),
    # path('password-reset-done/', PasswordResetDoneView.as_view(), name='account_reset_password_done'),
    #
    # path('reset/<uidb64>/<token>/', auth_views.PasswordResetConfirmView.as_view(), name='password_reset_confirm'),
    # path('password-reset-key/<uidb36>/<key>/', PasswordResetFromKeyView.as_view(),
    #      name='account_reset_password_from_key'),
    # path('password-reset-key-done/', PasswordResetFromKeyDoneView.as_view(),
    #      name='account_reset_password_from_key_done'),
    # path('email-verification-sent/', EmailVerificationSentView.as_view(), name='account_email_verification_sent'),
]