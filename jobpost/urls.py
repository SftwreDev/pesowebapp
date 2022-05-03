from django.urls import path


from .views import *

urlpatterns = [
    path("jobs", jobpost_list, name="jobpost_list"),
    path("jobs-detail/<int:pk>", jobpost_detail, name="jobdetail"),
    path("jobs-posted", job_posted, name="job_posted"),
    path("jobs-applicants", applicants, name="applicants"),
    path("view-applicants/<int:pk>", view_applicants, name="view_applicants"),
    path("disapproved-applicants/<int:pk>", disapproved_applicants, name="disapproved_applicants"),
    path("approved-applicants/<int:pk>", approved_applicants, name="approved_applicants"),
    path("applied-jobs", applied_jobs, name="applied_jobs"),
    path("close-jobs/<int:pk>", close_job, name="close_job"),
    path("open-jobs/<int:pk>", open_job, name="open_job"),
]