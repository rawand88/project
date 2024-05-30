from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login as auth_login, logout as auth_logout
from django.contrib.auth.models import User
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from .models import Students, Courses, studentsReg, CourseSchedules
from .forms import SignupForm, LoginForm, CourseRegistrationForm
from django.db.models import Q
from datetime import datetime, timedelta, date

def register(request):
    if request.method == 'POST':
        form = SignupForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data['username']
            email = form.cleaned_data['email']
            password = form.cleaned_data['password']
            if User.objects.filter(email=email).exists():
                messages.info(request, 'Email is already exists')
            else:
                user = User.objects.create_user(username=username, email=email, password=password)
                user.save()
                user_login = authenticate(username=username, password=password)
                if user_login is not None:
                    auth_login(request, user_login)
                    Students.objects.create(user=user)
                    return redirect('/')
                else:
                    messages.error(request, 'User authentication failed')
        else:
            messages.error(request, 'Form is not valid')
    else:
        form = SignupForm()
    return render(request, 'webapp/register.html', {'form': form})

def login(request):
    if request.method == 'POST':
        form = LoginForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data['username']
            password = form.cleaned_data['password']
            user = authenticate(username=username, password=password)
            if user is not None:
                auth_login(request, user)
                return redirect('/')
            else:
                messages.info(request, 'error in Username or password')
        else:
            messages.error(request, 'Form is not valid')
    else:
        form = LoginForm()
    return render(request, 'webapp/login.html', {'form': form})

@login_required(login_url='/login')
def logout_view(request):
    auth_logout(request)
    return redirect('/login')
@login_required(login_url='/login')
def home(request):
    courses = Courses.objects.all()
    search_query = ''
    if request.method == 'POST':
        form = CourseRegistrationForm(request.POST)
        if form.is_valid():
            search_query = form.cleaned_data["query"]
            courses = Courses.objects.filter( Q(code__icontains=search_query) | Q(name__icontains=search_query))
    else:
        form = CourseRegistrationForm()
    student = Students.objects.get(user = request.user)

    # Notification found
    my_courses = studentsReg.objects.filter(student_id=student)
    now = datetime.now()
    notefication = []
    for s in my_courses:
        c = Courses.objects.get(code=s.course_id.code)
        course_start_datetime = datetime.combine(date.today(), c.schedule_id.start_time)
        difference = course_start_datetime - now - timedelta(minutes=20)
        if difference.total_seconds() < 60:
            notefication.append({'course_name': c.name, 'start_time': c.schedule_id.start_time})


    return render(request, 'webapp/home.html', context={'courses': courses, 'search_query': search_query, 'form': form,'notifications':notefication})

@login_required(login_url='/login')
def select_course(request, pk):
    course = Courses.objects.get(code=pk)
    user = request.user
    student = Students.objects.get(user=user)
    
    if studentsReg.objects.filter(course_id=course, student_id=student).exists():
        messages.info(request, 'You are already registered.')
        return redirect(f'/courseDetails/{course.code}')
    elif studentsReg.objects.filter(course_id=course).count() >= course.capacity:
        messages.info(request, 'Course is full.')
        return redirect(f'/courseDetails/{course.code}')

    else:
        schedule_new_course = course.schedule_id.start_time
        if studentsReg.objects.filter(student_id=student, course_id__schedule_id__start_time=schedule_new_course).exists():
            messages.info(request, 'Conflict with another course.')
        else:
            studentsReg.objects.create(course_id=course, student_id=student)
            messages.success(request, 'Successfully registered for the course.')
    return redirect(f'/courseDetails/{pk}')

@login_required(login_url='/login')
def courseDetails(request, pk):
    course = Courses.objects.filter(code=pk).first()
    student = Students.objects.filter(user=request.user).first()
    
    course_student_count = studentsReg.objects.filter(course_id=course).count()
    return render(request, 'webapp/courseDetails.html', {'course': course, 'prerequieits': course.prerequisites.all(), 'spots':course.capacity - course_student_count })

@login_required(login_url='/login')
def my_courses(request):
    student = Students.objects.get(user=request.user)
    my_schedule = studentsReg.objects.filter(student_id=student)
    courses = [reg.course_id for reg in my_schedule]
    return render(request, 'webapp/my-courses.html', {'courses': courses})

def remove_course(request,pk):
    course = Courses.objects.get(code=pk)
    student = Students.objects.get(user= request.user)
    studentsReg.objects.get(course_id = course, student_id = student).delete()
    return redirect('/my-courses')
 