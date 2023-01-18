from django.urls import path
from django.contrib.auth import views as auth_views
from . import views

urlpatterns = [
    path(
        'personal_cabinet/', views.PersonalCabinetView.as_view(template_name='users/personal_cabinet.html'),
        name='personal-cabinet'
    ),
    path(
        'personal_cabinet/previous-flights',
        views.PersonalCabinetView.as_view(template_name='users/personal_cabinet_previous.html'),
        name='personal-cabinet-previous'
    ),
    path('register/', views.register, name='register'),
    path('login/', auth_views.LoginView.as_view(template_name='users/login.html'), name='login'),
    path('logout/', auth_views.LogoutView.as_view(template_name='users/logout.html'), name='logout'),
    path(
         'password-reset/',
         auth_views.PasswordResetView.as_view(template_name='users/password_reset.html'),
         name='password_reset'
    ),

    path(
        'password_reset/done/',
        auth_views.PasswordResetDoneView.as_view(template_name='users/password_reset_done.html'),
        name='password_reset_done'
    ),
    path('reset/<uidb64>/<token>/',
         auth_views.PasswordResetConfirmView.as_view(template_name="users/password_reset_confirm.html"),
         name='password_reset_confirm'),
    path('reset/done/',
         auth_views.PasswordResetCompleteView.as_view(template_name='users/password_reset_complete.html'),
         name='password_reset_complete'),
    # path('password_reset/done', auth_views.PasswordResetDoneView)
]
