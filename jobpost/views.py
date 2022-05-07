from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required

from .models import *
from .filters import *
from .forms import *
from applicant.forms import *
from applicant.models import *
from authentication.models import *
from .utils import *

@login_required(login_url="login")
def jobpost_list(request):
    """
        Function for Job Post list page
    """
    template_name = "jobpost/jobpost_list.html"
    obj = JobPost.objects.filter(status="Active").order_by("-created_at")
    filters  = JobPostFilter(request.GET, queryset=obj)
    forms = JobPostFormView(request.POST or None)
    if forms.is_valid():
        forms.save(commit=False)
        forms.instance.status = "Active"
        forms.instance.posted_by_id = request.user.id
        forms.save()
        return redirect('jobpost_list')
    context = {
        "obj": obj,
        "filters" : filters,
        "forms" : forms
    }
    return render(request, template_name, context)

@login_required(login_url="login")
def jobpost_detail(request, pk):
    template_name = "jobpost/jobpost_detail.html"
    jobs = JobPost.objects.get(id=pk)
    applicant_forms = ApplyJobForm(request.POST or None, request.FILES or None)
    try:
        status = ApplicationForm.objects.get(jobs_id=jobs.id, user_id=request.user.id)
    except Exception as e:
        status = ""
        print(e)
    check_file = ApplicantRequirement.objects.filter(jobs_id=pk).count()

    if check_file == 0:
        available_files = False
    else:
        available_files = True

    if applicant_forms.is_valid():
        applicant_forms.save(commit=False)
        applicant_forms.instance.user_id = request.user.id
        applicant_forms.instance.jobs_id = pk
        applicant_forms.already_applied = True
        applicant_forms.approved = "Pending"
        applicant_forms.save()
        return redirect('jobpost_list')
    
    try:
        already_apply = ApplicationForm.objects.get(jobs_id=pk, user_id=request.user.id)
        if already_apply is not None:
            applied_already = True
    except Exception as e:
        applied_already = False
        print(e)
    context = {
        "jobs" : jobs,
        "applicant_forms" : applicant_forms,
        "applied_already" : applied_already,
        "status" : status,
        "available_files" : available_files
    }
    return render(request, template_name, context)

@login_required(login_url="login")
def job_posted(request):
    template_name = "jobpost/jobpost_posted.html"
    obj = JobPost.objects.filter(posted_by=request.user.id).order_by("-created_at")
    filters  = JobPostFilter(request.GET, queryset=obj)
    forms = JobPostFormView(request.POST or None)


    if forms.is_valid():
        forms.save(commit=False)
        forms.instance.status = "Active"
        forms.instance.posted_by_id = request.user.id
        forms.save()
        return redirect('job_posted')

    context = {
        "obj": obj,
        "filters" : filters,
        "forms" : forms
    }
    return render(request, template_name, context)

@login_required(login_url="login")
def applicants(request):
    template_name = "jobpost/applicants.html"
    obj = JobPost.objects.select_related().filter(posted_by=request.user.id)

    for jobs in obj:
        applicants = ApplicationForm.objects.select_related().filter(jobs_id=jobs.id)
        
        context = {
            "applicants" : applicants
        }
        return render(request, template_name, context)
    
    return render(request, template_name)

@login_required(login_url="login")
def view_applicants(request, pk):
    template_name = "jobpost/view_applicants.html"
    applicants = ApplicationForm.objects.get(id=pk)
    user  = Applicant.objects.get(user_id=applicants.user_id)
    requirements = ApplicantRequirement.objects.filter(user_id=applicants.user_id)
    try:
        check_file = ApplicantRequirement.objects.filter(id=pk)
        available_files = True
    except Exception as e:
        available_files = False
    context = {
        "applicants" : applicants,
        "user" : user,
        "requirements" : requirements,
        "available_files" : available_files
        }
    return render(request, template_name, context)

@login_required(login_url="login")
def approved_applicants(request, pk):
    obj = ApplicationForm.objects.filter(id=pk).update(approved="Approved")
    applicant = ApplicationForm.objects.get(id=pk)
    send_email(applicant.user.email, applicant.user.first_name,  "Approved")
    return redirect("applicants")

def disapproved_applicants(request, pk):
    obj = ApplicationForm.objects.filter(id=pk).update(approved="Disapproved")
    applicant = ApplicationForm.objects.get(id=pk)
    send_email(applicant.user.email, applicant.user.first_name,  "Disapproved")
    return redirect("applicants")

def applied_jobs(request):
    template_name = "jobpost/applied_jobs.html"
    obj = ApplicationForm.objects.filter(user_id=request.user.id)

    context = {
        "obj": obj,
    }
    return render(request, template_name, context)


@login_required(login_url="login")
def close_job(request, pk):
    obj = JobPost.objects.filter(id=pk).update(status="Inactive")
    return redirect("job_posted")

def open_job(request, pk):
    obj = JobPost.objects.filter(id=pk).update(status="Active")
    return redirect("job_posted")