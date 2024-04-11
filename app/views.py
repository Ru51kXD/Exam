from django.views import View
from django.views.generic import CreateView, ListView,DeleteView
from django.shortcuts import redirect
from .forms import SignUpForm, TaskForm
from .models import CustomUser, Task
from django.urls import reverse_lazy
from django.contrib.messages.views import SuccessMessageMixin 
from django.contrib.auth.tokens import default_token_generator
from django.contrib import messages
from django.core.mail import send_mail
from django.contrib.auth.views import LoginView, LogoutView
from django.contrib.auth.mixins import LoginRequiredMixin




class SignUpView(SuccessMessageMixin, CreateView):
    model = CustomUser
    form_class = SignUpForm
    template_name = 'signup.html'
    success_url = reverse_lazy('task')
    success_message = 'Account created successfully'
    
    def send_verification_email(self, user):
        token = default_token_generator.make_token(user)
        verify_url = self.request.build_absolute_uri(f'/verify/{user.pk}/{token}/')
        subject = 'Verify your email'
        message = f'Hello {user.username}, please click the link below to verify your email:\n\n{verify_url}'
        send_mail(subject, message, 'sender@example.com', [user.email])

    def form_valid(self, form):
        response = super().form_valid(form)
        user = self.object  
        user.is_active = False
        user.save()
        self.send_verification_email(self.object)
        return response
    
class VerifyEmailView(View):
    def get(self, request, user_pk, token):
        user = CustomUser.objects.get(pk=user_pk)
        if default_token_generator.check_token(user, token):
            user.is_active = True
            user.save()
            messages.success(request, 'Your email has been verified')
            return redirect('task')
        else:
            messages.error(request, 'Invalid verification link')
            return redirect('task')

class Login(SuccessMessageMixin, LoginView):
    template_name = 'login.html'
    next_page = reverse_lazy('task')
    success_message = 'You are logged in successfully'
    
class Logout(LogoutView):
    next_page = reverse_lazy('task')
        


class TaskView(ListView,SuccessMessageMixin):
    model = Task
    context_object_name = 'tasks'
    template_name = 'task.html'
    success_message = 'Task created successfully'


class CreateTask(LoginRequiredMixin, CreateView):
    model = Task
    login_url = reverse_lazy('login')
    fields = ['task','title']
    success_url = reverse_lazy('task')
    template_name = 'create.html'

class TaskDeleteView(DeleteView):
    model = Task
    success_url = reverse_lazy('task')
