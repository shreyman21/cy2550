from django.http import HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse
from django.utils.safestring import mark_safe
from .models import StudentUser, Admin
from django.contrib import messages
from django.db import connection
import datetime
import re


today = datetime.datetime.now()
this_year = today.year
next_year = today.year + 1

try:
    cbw = Admin.objects.get(username="cbw")
except:
    try:
        cbw = Admin.objects.create(username="cbw", password="NoOneCanEverGuessThisIncrediblyLongPasswordLOL0192837465")
    except:
        exit    

def index(request):
    return render(request, 'frontend/index.html')

def login(request):
    return render(request, 'frontend/login.html')

def login_submit(request):
    username = request.POST.get('username')
    password = request.POST.get('password')
    correct_password = True

    if username:
        sql_query_user= "SELECT * FROM frontend_studentuser WHERE username='"+username+"'AND password='"+password+"'"
        try:
            val=StudentUser.objects.raw(sql_query_user)
        except:
            messages.warning(request, 'Error with login, please try again')
            return render(request, 'frontend/login.html')
        if val:
            student = StudentUser.objects.get(username=username)
            student_password = student.password
            with connection.cursor() as cursor:
                cursor.execute(f"UPDATE frontend_studentuser SET logged_in = TRUE WHERE username='"+student.username+"'")
            if student_password != password:
                correct_password = False
            request.session['login_info'] = request.POST
            student_postlogin = StudentUser.objects.get(username=username)
            return render(request, 'frontend/homepage.html', context={'logged_in': student_postlogin.logged_in, 'correct_password':correct_password})
        else:
            messages.warning(request, 'Error with password, please try again')
            return render(request, 'frontend/login.html')
    else:
        return render(request, 'frontend/login.html')


def login_results(request):
    return render(request, 'frontend/homepage.html', context={'logged_in': request.session.get('login_info')['logged_in']}) 
       
def home(request):
    logged_in = retrieve_loggedin(request)
    return render(request, 'frontend/homepage.html', context={'logged_in': logged_in, 'correct_password': True})

def feedback(request):
    logged_in = retrieve_loggedin(request)
    return render(request, 'frontend/feedback.html', context={'logged_in': logged_in})

def feedback_submit(request):
    request.session['old_post'] = request.POST
    return HttpResponseRedirect(reverse('frontend:feedback_results'))

def feedback_results(request):
    old_post = request.session['old_post']
    logged_in = retrieve_loggedin(request)
    return render(request, 'frontend/feedback_submit.html', context={'feedback': mark_safe(old_post['feedback_input']), 'logged_in': logged_in})

def ta_app(request):
    logged_in = retrieve_loggedin(request)
    return render(request, 'frontend/ta_application.html', context={'logged_in': logged_in})

def ta_app_submit(request):
    request.session['post'] = request.POST
    return HttpResponseRedirect(reverse('frontend:ta_app_results'))

def ta_app_results(request):
    logged_in = retrieve_loggedin(request)
    return render(request, 'frontend/ta_application_results.html', context={'logged_in': logged_in})

def create_account(request):
    return render(request, 'frontend/create_account.html')

def create_account_submit(request):
    username = request.POST.get('username')
    password = request.POST.get('password')

    if re.match(r'^[A-Za-z0-9]', username) and re.match(r'^[A-Za-z0-9]', password):
        with connection.cursor() as cursor:
            cursor.execute("SELECT * FROM frontend_studentuser WHERE username='"+username+"'")
            row = cursor.fetchone()
        if row is not None:
            messages.warning(request, 'Account with that username already exists')
            return render(request, 'frontend/create_account.html')
        else:
            sql_query_add = "INSERT INTO frontend_studentuser(username, password, logged_in) VALUES ('"+username+"', '"+password+"', 'FALSE')"
            with connection.cursor() as cursor:
                cursor.execute(sql_query_add)
            return render(request, 'frontend/login.html')
    else:
        messages.warning(request, 'Only alphanumeric characters are allowed for username and password.')    
        return render(request, 'frontend/create_account.html')
    
def logout(request):
    username = request.session.get('login_info')['username']
    student = StudentUser.objects.get(username=username)
    with connection.cursor() as cursor:
        cursor.execute(f"UPDATE frontend_studentuser SET logged_in = FALSE WHERE username='"+student.username+"'")
    return render(request, 'frontend/login.html')

def retrieve_loggedin(request):
    try:
        username = request.session.get('login_info')['username']
        student = StudentUser.objects.get(username=username)
        return student.logged_in
    except:
        return False

def forgot_pw(request):
    return render(request, 'frontend/forgot_password.html')

def forgot_pw_submit(request):
    request.session['user_submit'] = request.POST
    return HttpResponseRedirect(reverse('frontend:forgot_pw_kbq'))

def forgot_pw_kbq(request):
    previous = request.session['user_submit']
    return render(request, 'frontend/forgot_password_kbq.html', context={'username': mark_safe(previous['uname'])})

def forgot_pw_kbq_submit(request):
    request.session['user_kbq'] = request.POST
    return HttpResponseRedirect(reverse('frontend:forgot_pw_kbq_success'))

def forgot_pw_kbq_success(request):
    previous = request.session['user_kbq']
    kbq_success = False
    if str(previous['answer1']).lower() == "blue" and \
        (str(previous['answer2']).lower() == "university of california, santa barbara" or \
        str(previous['answer2']).lower() == "uc santa barbara" or \
        str(previous['answer2']).lower() == "ucsb") and \
        (str(previous['answer3']).lower() == "computer science" or \
        str(previous['answer3']).lower() == "cs"):
        kbq_success = True

    return render(request, 'frontend/forgot_password_kbq_success.html', context={'success': kbq_success})

def password_change_successful(request):
    password = request.POST.get('password')
    cbw_user = Admin.objects.get(username="cbw")
    cbw_user.password = password
    cbw_user.save()
    
    return render(request, 'frontend/password_change_successful.html')

def submit_hours(request):
    logged_in = retrieve_loggedin(request)
    return render(request, 'frontend/submit_hours.html', context={'logged_in': logged_in})

def submit_hours_submit(request):
    request.session['hours_submission'] = request.POST
    return HttpResponseRedirect(reverse('frontend:submit_hours_results'))

def submit_hours_results(request):
    logged_in = retrieve_loggedin(request)
    try:
        hours_submission = request.session['hours_submission']
        total_hours = int(hours_submission['sunday']) + int(hours_submission['monday']) + int(hours_submission['tuesday']) + int(hours_submission['wednesday']) + int(hours_submission['thursday']) + int(hours_submission['friday']) + int(hours_submission['saturday'])
        
        greater_than_max = int(total_hours) > int(hours_submission['max_hours']) 
        max_greater_than_20 = int(hours_submission['max_hours']) > int(20) and int(total_hours) > 20

        return render(request, 'frontend/submit_hours_results.html', context={'greater_than_max': greater_than_max, 'max_greater_than_20': max_greater_than_20, 'logged_in': logged_in})
    except:
        return render(request, 'frontend/submit_hours.html', context={'logged_in': logged_in})
    
def scholarships(request):
    logged_in = retrieve_loggedin(request)
    return render(request, 'frontend/scholarships.html', context={'logged_in': logged_in, 'year':this_year, 'next_year': next_year})

def scholarships_too_late(request):
    logged_in = retrieve_loggedin(request)
    return render(request, 'frontend/scholarships_too_late.html', context={'logged_in': logged_in, 'year':this_year, 'next_year': next_year})

def scholarships_next_year(request):
    logged_in = retrieve_loggedin(request)
    return render(request, 'frontend/scholarships_next_year.html', context={'logged_in': logged_in, 'year':this_year, 'next_year': next_year})

def scholarships_next_year_sparkbear(request):
    logged_in = retrieve_loggedin(request)
    return render(request, 'frontend/scholarships_next_year_sparkbear.html', context={'logged_in': logged_in, 'next_year': next_year})

def scholarships_next_year_cooper(request):
    logged_in = retrieve_loggedin(request)
    return render(request, 'frontend/scholarships_next_year_cooper.html', context={'logged_in': logged_in})

def scholarships_click_here(request):
    logged_in = retrieve_loggedin(request)
    return render(request, 'frontend/scholarships_first_click.html', context={'logged_in': logged_in, 'year':this_year, 'next_year': next_year})

def scholarships_winner(request):
    logged_in = retrieve_loggedin(request)
    return render(request, 'frontend/scholarships_winner.html', context={'logged_in': logged_in, 'year':this_year, 'next_year': next_year})

def admin(request):
    logged_in = retrieve_loggedin(request)
    return render(request, 'frontend/admin.html', context={'logged_in': logged_in})

def admin_submit(request):
    logged_in = retrieve_loggedin(request)
    username = request.POST.get('username')
    password = request.POST.get('password')

    if username:
        try:
            val = Admin.objects.get(username=username)
            if val:
                if val.password == password:
                    return render(request, 'frontend/admin_login_success.html', context={'logged_in': logged_in})
                else:
                    messages.warning(request, 'Error with admin password, please try again')
                    return render(request, 'frontend/admin.html')
        except:
            messages.warning(request, 'Error with admin login, please try again')
            return render(request, 'frontend/admin.html')
        
    else:
        return render(request, 'frontend/admin.html')
    
