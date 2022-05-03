from django.shortcuts import render, get_object_or_404
from django.shortcuts import redirect
from django.views.generic import CreateView
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages

from .models import *
from .forms import *
from .utils import *
# Create your views here.


def accounts(request):
    template_name = "user_accounts/accounts.html"
    accounts = User.objects.all()
    context = {
        "accounts": accounts
    }
    return render(request, template_name, context)


def viewprofile(request):
    template_name = "profile/profile.html"
    return render(request, template_name)


def user_update(request, pk):
    template_name = "user_accounts/update_account.html"
    user = get_object_or_404(User, pk=pk)
    form = AdminSignUpForm(request.POST or None, instance=user)
    if form.is_valid():
        form.save()
        return redirect("/")
    context = {
        "form": form
    }
    return render(request, template_name, context)


def profile_update(request, pk):
    template_name = "user_accounts/update_account.html"
    user = get_object_or_404(User, pk=pk)
    form = UpdateForm(request.POST or None, instance=user)
    if form.is_valid():
        form.save()
        return redirect("/")
    context = {
        "form": form
    }
    return render(request, template_name, context)


def user_delete(request, pk):
    user = User.objects.filter(id=pk).update(status=False)
    return redirect("/")


class AdminSignUpView(CreateView):
    model = User
    form_class = AdminSignUpForm
    template_name = 'registration/signup_form.html'

    def get_context_data(self, **kwargs):
        kwargs['user_type'] = 'admin'
        return super().get_context_data(**kwargs)

    def form_valid(self, form):
        user = form.save()
        return redirect('/')


class EmployerSignUpView(CreateView):
    model = Employer
    form_class = EmployerSignUpForm
    template_name = 'registration/signup_form.html'

    def get_context_data(self, **kwargs):
        kwargs['user_type'] = 'employer'
        return super().get_context_data(**kwargs)

    def form_valid(self, form):
        user = form.save(commit=False)
        user.role = 'employer'
        user.is_superuser = True
        user.is_staff = True
        user.save()
        print("USER ID", user.id)
        full_name = user.first_name
        email = encrypt_email(user.email)
        link = f"http://localhost:8000/verify-email/{email}"
        send_email(user.email, full_name, link)
        employer = Employer.objects.create(
            user_id=user.id, 
            company_name=form.cleaned_data['company_name'], 
            company_address=form.cleaned_data['company_address'], 
            business_nature=form.cleaned_data['business_nature'],
            status = "Active"
            )
        
        return redirect('email_sent')


class ApplicantSignUpView(CreateView):
    model = Applicant
    form_class = ApplicantSignUpForm
    template_name = 'registration/signup_form.html'

    def get_context_data(self, **kwargs):
        kwargs['user_type'] = 'applicant'
        return super().get_context_data(**kwargs)

    def form_valid(self, form):
        user = form.save(commit=False)
        user.role = 'applicant'
        user.save()
        print("USER ID", user.id)
        full_name = user.first_name
        email = encrypt_email(user.email)
        link = f"http://localhost:8000/verify-email/{email}"
        send_email(user.email, full_name, link)
        employer = Applicant.objects.create(
            user_id=user.id, 
            address=form.cleaned_data['address'], 
            working_exp=form.cleaned_data['working_exp'], 
            prev_employer=form.cleaned_data['prev_employer'],
            birthdate=form.cleaned_data['birthdate'],
            age=form.cleaned_data['age'],
            status = "Active"
            )
        return redirect('email_sent')


def employer_profile(request):
    template_name = "employer_profile.html"
    profile = Employer.objects.get(user__id = request.user.id)

    context = {
        "profile" : profile
    }
    return render(request, template_name,context)

def applicant_profile(request):
    template_name = "applicant_profile.html"
    profile = Applicant.objects.get(user__id = request.user.id)

    context = {
        "profile" : profile
    }
    return render(request, template_name,context)


def login_page(request):
    form = LoginForm()
    message = ''
    if request.method == 'POST':
        form = LoginForm(request.POST or None)
        if form.is_valid():
            user = authenticate(
                email=form.cleaned_data['email'],
                password=form.cleaned_data['password'],
            )
            check_verified = User.objects.filter(email=form.cleaned_data['email'])
            for check in check_verified:
                if check.is_verified:
                    if user is not None:
                        login(request, user)
                        return redirect('/')
                    else:
                        messages.error(request, 'Invalid email address or password')
                        return redirect('login')
                else:
                    messages.error(request, 'Email not verified')
                    return redirect('login')
    return render(
        request, 'registration/login.html', context={'form': form})

def logout_user(request):
    logout(request)
    return redirect('login')


def verify_email(request, str):
    email = decrypt_email(str)
    print(email)
    user = User.objects.filter(email=email).update(is_verified=True)
    return redirect('login')


def email_sent(request):
    template_name = "email_sent.html"

    return render(request, template_name)