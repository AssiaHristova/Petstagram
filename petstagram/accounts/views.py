from django.contrib.auth import logout, login, authenticate
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.views import LoginView
from django.core.exceptions import ValidationError
from django.shortcuts import render, redirect
from django.urls import reverse_lazy
from django.views.generic import CreateView, FormView, UpdateView

from petstagram.accounts.forms import LoginForm, RegisterForm, ProfileForm, LoginForm2
from petstagram.accounts.models import Profile
from petstagram.pets.models import Pet


class LogInView(LoginView):
    authentication_form = LoginForm2
    template_name = 'accounts/login.html'
    success_url = reverse_lazy('landing page')



class RegisterView(CreateView):
    form_class = RegisterForm
    template_name = 'accounts/signup.html'
    success_url = reverse_lazy('landing page')

    def form_valid(self, form):
        registered_user = super().form_valid(form)
        login(self.request, self.object)
        return registered_user


def logout_user(request):
    logout(request)
    return redirect('landing page')


class ProfileDetailsView(LoginRequiredMixin, FormView):
    template_name = 'accounts/user_profile.html'
    form_class = ProfileForm
    success_url = reverse_lazy('profile details')
    object = None

    def get(self, request, *args, **kwargs):
        self.object = Profile.objects.get(pk=request.user.id)
        return super().get(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        self.object = Profile.objects.get(pk=request.user.id)
        return super().post(request, *args, **kwargs)

    def form_valid(self, form):
        self.object.profile_image = form.cleaned_data['profile_image']
        self.object.save()
        return super().form_valid(form)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        context['pets'] = Pet.objects.filter(user_id=self.request.user.id)
        context['profile'] = self.object

        return context



