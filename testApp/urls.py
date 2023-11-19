from django.urls import path
from .views import *

urlpatterns = [
    path('school-stats/', SchoolStatsView.as_view(), name='school-stats'),
    path('enrolled/', EnrolledCoursesView.as_view(),name='enrolled'),
    # Other URL patterns
]
