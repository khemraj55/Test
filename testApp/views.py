from django.shortcuts import render

# Create your views here.
from django.http import JsonResponse
from django.db.models import Count, OuterRef, Subquery
from django.views import View
from .models import School, Student, Course, Enrolment

class SchoolStatsView(View):
    def get(self, request, *args, **kwargs):
        # Annotate each school with the count of students enrolled in courses
        schools_with_student_count = School.objects.annotate(
            student_count=Count('students')
        )

        # Subquery to get the count of courses for each school
        subquery = Course.objects.filter(school=OuterRef('pk')).values('school').annotate(course_count=Count('pk')).values('course_count')

        # Annotate each school with the count of courses
        schools_with_course_count = schools_with_student_count.annotate(
            course_count=Subquery(subquery)
        )

        # Convert queryset to a list of dictionaries for JsonResponse
        schools_data = [
            {
                'id': school.id,
                'name': school.name,
                'location': school.location,
                'student_count': school.student_count,
                'course_count': school.course_count
            }
            for school in schools_with_course_count
        ]

        return JsonResponse({'schools': schools_data})
    

from django.db.models import OuterRef, Subquery, Q
from django.http import JsonResponse
from django.views import View
from .models import School, Student, Course, Enrolment

class EnrolledCoursesView(View):
    def get(self, request, *args, **kwargs):
        # Subquery to get a list of course IDs in which a student is enrolled
        subquery = Enrolment.objects.filter(
            student=OuterRef('pk')
        ).values('course').annotate(enrolment_count=Count('pk')).values('course')

        # Query to get students and courses they are enrolled in
        students_with_enrolled_courses = Student.objects.annotate(
            enrolled_course_ids=Subquery(subquery)
        ).prefetch_related('enrolments__course')

        # Convert queryset to a list of dictionaries for JsonResponse
        result_data = [
            {
                'student_id': student.id,
                'student_name': student.name,
                'enrolled_courses': list(student.enrolments.values_list('course__title', flat=True))
            }
            for student in students_with_enrolled_courses
        ]

        return JsonResponse({'enrolled_courses': result_data})

