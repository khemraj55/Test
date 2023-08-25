from django.db import models

class Student(models.Model):
    name = models.CharField(max_length=255)
    email = models.EmailField()
    age=models.models.IntegerField()
    
class Course(models.Model):
    title = models.CharField(max_length=255)
    instructor = models.ForeignKey(Student, on_delete=models.CASCADE)
    fees= models.models.IntegerField()
    couse_name=models.models.CharField(max_length=50)

class Enrollment(models.Model):
    student = models.ForeignKey(Student, on_delete=models.CASCADE)
    course = models.ForeignKey(Course, on_delete=models.CASCADE)
    total_fees=models.models.IntegerField()

    

    