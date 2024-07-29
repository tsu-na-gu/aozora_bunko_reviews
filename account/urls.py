from django.urls import path
from account.views import CustomLoginView, CustomLogoutView, CustomRegisterView, ProfileView

urlpatterns = [
    path('login/', CustomLoginView.as_view(), name='login'),
    path('logout/', CustomLogoutView.as_view(), name='logout'),
    path('signup/', CustomRegisterView.as_view(), name='signup'),
    path('profile/', ProfileView.as_view(), name='profile'),
]