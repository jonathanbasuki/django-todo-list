from django.shortcuts import render, redirect
from django.views.generic.list import ListView # import ListView functional // built-in queryset
from django.views.generic.detail import DetailView # import DetailView functional // built-in queryset
from django.views.generic.edit import CreateView, UpdateView, DeleteView, FormView # import CreateView, UpdateView, DeleteView, FormView functional // built-in queryset
from django.urls import reverse_lazy # import reverse_lazy // redirect user to different page after submit form
from django.contrib.auth.views import LoginView # import django login view // built-in view
from django.contrib.auth.mixins import LoginRequiredMixin # import django mixin to restrict user // built-in mixin
from django.contrib.auth.forms import UserCreationForm # import django method to create user // built-in method 
from django.contrib.auth import login # once user created an account their will be logged in automatically // built-in method
from .models import Task # import Task model // models.py

# create CustomLoginView inherit from LoginView
class CustomLoginView(LoginView):
	template_name = 'base/login.html'
	fields = '__all__'
	redirect_authenticated_user = True

	# override success_url
	def get_success_url(self):
		return reverse_lazy('tasks');

# create RegisterPage inherit from FormView
class RegisterPage(FormView):
	template_name = 'base/register.html'
	form_class = UserCreationForm
	redirect_authenticated_user = True
	success_url = reverse_lazy('tasks')

	# override RegisterPage built-in function
	def form_valid(self, form):
		user = form.save() # save user input
		if user is not None: # check user input redirect and log user in
			login(self.request, user) 

		return super(RegisterPage, self).form_valid(form)

	# method to redirect user back // restrict logged in user to go back to login and register page
	def get(self, *args, **kwargs):
		if self.request.user.is_authenticated:
			return redirect('tasks')
		return super(RegisterPage, self).get(*args, **kwargs)

# create TaskList inherit from ListView
class TaskList(LoginRequiredMixin, ListView):
	model = Task # use Task model
	context_object_name = 'tasks' # override the default queryset object name // default = 'object_list'

	# override ListView built-in function // so user only get their own tasks
	def get_context_data(self, **kwargs):
		context = super().get_context_data(**kwargs)
		context['tasks'] = context['tasks'].filter(user = self.request.user) # filter tasks based on user login
		context['count'] = context['tasks'].filter(complete = False).count()

		# search logic
		search_input = self.request.GET.get('keyword') or '' # get keyword from user
		if search_input:
			context['tasks'] = context['tasks'].filter(title__startswith = search_input) # filter title that match with keyword 

		context['search_input'] = search_input;

		return context

# create TaskDetail inherit from DetailView
class TaskDetail(LoginRequiredMixin, DetailView):
	model = Task # use Task model
	context_object_name = 'task' # override the default queryset object name // default = 'object'
	template_name = 'base/task.html' # override the default queryset template name // default = 'task_detail.html'

# create TaskCreate inherit from CreateView
class TaskCreate(LoginRequiredMixin, CreateView):
	model = Task # use Task model
	fields = ['title', 'description', 'complete'] # field that want to show in form // in this case show title, description, and complete input fields
	success_url = reverse_lazy('tasks') # send user back to the list after submit the form

	# override CreateView built-in function
	def form_valid(self, form):
		form.instance.user = self.request.user # set input form to logged in user

		return super(TaskCreate, self).form_valid(form)

# create TaskUpdate inherit from CreateView
class TaskUpdate(LoginRequiredMixin, UpdateView):
	model = Task # use Task model
	fields = ['title', 'description', 'complete'] # field that want to show in form // in this case show title, description, and complete input fields
	success_url = reverse_lazy('tasks') # send user back to the list after submit the form

# create TaskDelete inherit from DeleteView
class TaskDelete(LoginRequiredMixin, DeleteView):
	model = Task # use Task model
	context_object_name = 'task' # override the default queryset object name // default = 'object'
	success_url = reverse_lazy('tasks') # send user back to the list after submit the form