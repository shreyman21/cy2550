app_name="frontend"

from django.urls import path, include

from . import views

import datetime

today = datetime.datetime.now()
this_year = today.year
next_year = today.year + 1


urlpatterns = [
    path('admin/', views.admin, name='admin'),
    path('admin-submit/', views.admin_submit, name='admin_submit'),
    path('password-change-successful/', views.password_change_successful, name='admin_new_password_submit'),
    path('login/', views.login, name='login'),
    path('logout/', views.logout, name='logout'),
    path('login-submit/', views.login_submit, name='login_submit'),
    path('accounts/', include("django.contrib.auth.urls")),
    path('', views.home, name='home'),
    path('create-account/', views.create_account, name='create_account'),
    path('create-account-submit', views.create_account_submit, name='create_account_submit'),    
    path('logout/', views.index, name='logout'),
    path('ta-applications/', views.ta_app, name='ta_applications'),
    path('ta-application-results', views.ta_app_results, name='ta_application_results'),
    path('grades/', views.index, name='grades'),
    path('closed-course-petition/', views.index, name='closed_course_petition'),
    path('submit-hours/', views.submit_hours, name='submit_hours'),
    path('submit-hours-submit/', views.submit_hours_submit, name='submit_hours_submit'),
    path('submit-hours-results/', views.submit_hours_results, name='submit_hours_results'),
    path(f'scholarships/{this_year}', views.scholarships, name="scholarships"),
    path(f'scholarships/{this_year}/whoops-too-late', views.scholarships_too_late, name="scholarships_too_late"),
    path('feedback/', views.feedback, name='feedback'),
    path('feedback-submit/', views.feedback_submit, name='feedback_submit'),
    path('feedback-results/', views.feedback_results, name='feedback_results'),
    path('forgot-password/', views.forgot_pw, name='forgot_password'),
    path('forgot-password-submit', views.forgot_pw_submit, name='forgot_pw_submit'),
    path('forgot-password-kbq/', views.forgot_pw_kbq, name='forgot_pw_kbq'), 
    path('forgot-password-kbq-submit/', views.forgot_pw_kbq_submit, name='forgot_pw_kbq_submit'),
    path('forgot-password-kbq-success/', views.forgot_pw_kbq_success, name='forgot_pw_kbq_success'),
    path(f'scholarships/{next_year}', views.scholarships_next_year, name='scholarships_next_year'),
    path(f'scholarships/{next_year}/you-cannot-fool-us', views.scholarships_next_year_sparkbear, name='scholarships_next_year_sparkbear'),
    path(f'scholarships/{next_year}/first-click', views.scholarships_click_here, name='scholarships_first_click'),
    path(f'scholarships/{next_year}/cooper-good-boy', views.scholarships_next_year_cooper, name='scholarships_next_year_cooper'),
    path(f'scholarships/{next_year}/you-earned-it', views.scholarships_winner, name='scholarships_winner'),
    ]   