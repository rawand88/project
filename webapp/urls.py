from django.urls import path
from . import views




urlpatterns = [
    path('login/', views.login),
    path('register/', views.register),
    path('logout_view/', views.logout_view),
    path('courseDetails/<int:pk>', views.courseDetails),
    path('my-courses/', views.my_courses),
    path('', views.home),
    path('select-course/<int:pk>',views.select_course),
    path('removeCourse/<int:pk>',views.remove_course),


]
