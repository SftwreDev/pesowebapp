from django.shortcuts import get_object_or_404, render, redirect
from django.contrib.auth.decorators import login_required

from .models import *
from .forms import *

# Create your views here.

@login_required(login_url="login")
def announcement_list(request):
    template_name = "announcements/ann_list.html"
    announcement = Announcement.objects.all()
    context = {
        "announcement" : announcement
    }
    return render(request, template_name, context)

@login_required(login_url="login")
def announcement_add(request):
    template_name = "announcements/ann_create.html"
    form = AnnouncementForms(request.POST or None)
    if form.is_valid():
        form.save(commit=False)
        form.status = "Active"
        form.instance.posted_by_id = request.user.id
        form.save()
        return redirect("ann-list")
    context = {
       "form" :  form
    }
    return render (request, template_name, context)

@login_required(login_url="login")
def announcement_view(request, pk):
    template_name = "announcements/ann_view.html"
    announcement = Announcement.objects.get(id=pk)
    context = {
         "announcement" : announcement
    }
    return render (request, template_name, context)

@login_required(login_url="login")
def announcement_update(request, pk):
    template_name = "announcements/ann_update.html"
    announcement = get_object_or_404(Announcement, pk=pk)
    form = AnnouncementForms(request.POST or None, instance=announcement)
    if form.is_valid():
        form.save()
        return redirect("ann-list")
    context = {
       "form" :  form
    }
    return render (request, template_name, context)

@login_required(login_url="login")
def announcement_delete(request, pk):
    announcement = Announcement.objects.filter(id=pk)
    announcement.delete()
    return redirect("ann-list")


