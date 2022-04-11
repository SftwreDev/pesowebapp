from django.shortcuts import render

# Create your views here.
def homepage(request):
    template_name = "homepage/homepage.html"
    context = {
        "active" : "active"
    }
    return render(request, template_name, context)