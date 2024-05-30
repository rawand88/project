from django.db import models
from django.contrib.auth.models import User

class Students(models.Model):
    user = models.ForeignKey(User,on_delete=models.CASCADE)
    
class CourseSchedules(models.Model):
    id = models.IntegerField(primary_key=True)
    days = models.CharField(max_length=100)
    start_time = models.TimeField()
    end_time = models.TimeField()
    room_no = models.CharField(max_length=5)
    
class CoursePrerequisite(models.Model):
    course = models.ForeignKey('Courses', related_name='main_course', on_delete=models.CASCADE)
    prerequisite = models.ForeignKey('Courses', related_name='prerequisite_course', on_delete=models.CASCADE)

class Courses(models.Model):
    code = models.CharField(primary_key=True, max_length=10)
    name = models.CharField(max_length=100)
    description = models.CharField(max_length=255)
    prerequisites = models.ManyToManyField('self', through=CoursePrerequisite, symmetrical=False, related_name='related_to')
    instructor = models.CharField(max_length=30, default='')
    capacity = models.IntegerField(default=0)
    schedule_id = models.ForeignKey(CourseSchedules, on_delete=models.CASCADE, null=True,blank=True)

class studentsReg(models.Model):
    id = models.IntegerField(primary_key=True)
    student_id= models.ForeignKey(Students, on_delete=models.CASCADE)
    course_id = models.ForeignKey(Courses, on_delete=models.CASCADE)
