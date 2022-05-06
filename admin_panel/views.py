from django.shortcuts import render, redirect

from authentication.models import *

# Create your views here.

def admin_page(request):
    template_name = "admin/admin_panel.html"
    employer = Employer.objects.all()
    context = {
        "employer" : employer
    }
    return render(request, template_name, context)


def accept_account(request, pk):
    Employer.objects.filter(id=pk).update(accepted=True)
    return redirect("admin_page")

def unaccept_account(request, pk):
    Employer.objects.filter(id=pk).update(accepted=False)
    return redirect("admin_page")

def account_view(request, pk):
    template_name = "admin/account_detailed.html"
    employer = Employer.objects.get(id=pk)
    context = {
        "employer": employer
    }
    return render(request, template_name, context)