from django.shortcuts import render, redirect

from .models import *
from .forms import *
# Create your views here.

def appy_job(request):
    forms = ApplyJobForm(request.FILES or None)
    if forms.is_valid():
        forms.save(commit=False)
        forms.role = request.user.id
        forms.save()
        return redirect('jobpost_list')


def proceed_next_step(request, pk):
    template_name = "applicants/applied_job_status.html"
    jobs = JobPost.objects.get(id=pk)
    
    status = ApplicationForm.objects.get(jobs_id=jobs.id, user_id=request.user.id)
    if request.method == "POST":
        applicant_forms = ApplicantRequirementsForm(request.POST or None, request.FILES or None)
        files = request.FILES.getlist("file")
        if applicant_forms.is_valid():
            for file in files:
                ApplicantRequirement.objects.create(
                    file=file,
                    user_id=request.user.id,
                    requirements_type="requirements",
                    jobs_id=jobs.id
                )
            return redirect("proceed_next_step" , pk=pk)
    else:
        applicant_forms = ApplicantRequirementsForm(request.POST or None, request.FILES or None)
    
    requirements = ApplicantRequirement.objects.filter(user_id=request.user.id, jobs_id=jobs.id)
    check_file = ApplicantRequirement.objects.filter(jobs_id=pk).count()

    if check_file == 0:
        available_files = False
    else:
        available_files = True
    context = {
        "jobs" : jobs,
        "applicant_forms" : applicant_forms,
        "status" : status,
        "requirements" : requirements,
        "available_files" : available_files
    }

    return render(request, template_name, context)

