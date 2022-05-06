from django.shortcuts import render, redirect
from .forms import *
from .utils import *

# Create your views here.
def homepage(request):
    template_name = "homepage/homepage.html"
    form = ContactUsForm(request.POST or None)

    if request.method == 'POST':
        if form.is_valid():
            name = request.POST['name']
            email = request.POST['email']
            subject =request.POST['subject']
            message = request.POST['message']
            admin_email = "pesomalvar@gmail.com"
            send_email(admin_email, name, email, subject, message)
            return redirect('/')
        
    context = {
        "active" : "active",
        "form" : form
    }
    return render(request, template_name, context)



