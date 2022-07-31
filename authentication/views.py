from django.shortcuts import render, redirect
from django.contrib.auth import login, authenticate
from django.views.generic import View
from django.conf import settings
from .forms import LoginForm, SignupForm, ChangePasswordForm
from django.contrib.auth import update_session_auth_hash
from django.contrib.auth.decorators import login_required


class LoginPageView(View):
    template_name = 'authentication/login.html'
    form_class = LoginForm

    def get(self, request):
        form = self.form_class()
        message = ''
        return render(request, self.template_name, context={'form': form, 'message': message})

    def post(self, request):
        form = self.form_class(request.POST)
        if form.is_valid():
            user = authenticate(
                username=form.cleaned_data['username'],
                password=form.cleaned_data['password'],
            )
            if user is not None:
                login(request, user)
                return redirect('home')
        message = 'Identifiants invalides'
        return render(request, self.template_name, context={'form': form, 'message': message})


class SignupPageView(View):

    template_name = 'authentication/signup.html'
    form_class = SignupForm

    def get(self, request):
        form = self.form_class()
        return render(request, self.template_name, context={'form': form})

    def post(self, request):
        form = self.form_class(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect(settings.LOGIN_REDIRECT_URL)
        return render(request, self.template_name, context={'form': form})


class ChangePassword(View):
    template_name = 'authentication/password_change.html'
    form_class = ChangePasswordForm

    def get(self, request):
        form = self.form_class(request.user)
        message = ''
        return render(request, self.template_name, context={'form': form, 'message': message})

    def post(self, request):
        form = self.form_class(request.user, request.POST)
        if form.is_valid():
            user = form.save()
            update_session_auth_hash(request, user)
            return redirect('password-change-done')
        else:
            return render(request, self.template_name, context={'form': form})


class ChangePasswordDone(View):
    template_name = 'authentication/password_change_done.html'

    def get(self, request):
        return render(request, self.template_name)
