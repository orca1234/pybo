from django.contrib.auth import views as auth_views
from django.urls import path

from . import views

app_name = 'common'

urlpatterns = [
    path('login/', auth_views.LoginView.as_view(template_name='common/login.html'), name='login'),
    path('logout/', auth_views.LogoutView.as_view(), name='logout'),
    path('signup/', views.signup, name='signup'),

    path('profile/', views.profile, name='profile'),

    path('password_change/', auth_views.PasswordChangeView.as_view(
        template_name='common/password_change_form.html',
        success_url='/common/password_change/done/'
    ), name='password_change'),
    path('password_change/done/', auth_views.PasswordChangeDoneView.as_view(
        template_name='common/password_change_done.html'
    ), name='password_change_done'),
]