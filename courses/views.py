from django.shortcuts import render, redirect
from courses.models import Course, Lesson
from django.contrib import messages
from courses.forms import CourseModelForm, LessonModelForm
from django.views.generic.detail import DetailView
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from django.core.urlresolvers import reverse_lazy, reverse

class CourseDetailView(DetailView):
	model = Course
	template_name = "courses/detail.html"
	context_object_name = "course"
	success_url = reverse_lazy('index')

	def get_context_data(self, **kwargs):
		context = super(CourseDetailView, self).get_context_data(**kwargs)
		context['title'] = u'Course detail'
		pk = self.kwargs['pk']
		context['lessons'] = Lesson.objects.filter(course_id=pk)
		return context

class CourseCreateView(CreateView):
	model = Course
	template_name = "courses/add.html"
	context_object_name = "course"
	success_url = reverse_lazy('index')

	def get_context_data(self, **kwargs):
		context = super(CourseCreateView, self).get_context_data(**kwargs)
		context['title'] = u'Course creation'		
		return context

	def form_valid(self, form):
		application = form.save()
		message = u'Course %s has been successfully added.' % (application.name)
		messages.success(self.request, message)
		return super(CourseCreateView, self).form_valid(form)

class CourseUpdateView(UpdateView):
	model = Course
	template_name = "courses/edit.html"
	context_object_name = "course"
	#success_url = reverse_lazy('courses:edit', application.id)

	def get_context_data(self, **kwargs):
		context = super(CourseUpdateView, self).get_context_data(**kwargs)
		context['title'] = u'Course update'		
		return context

	def form_valid(self, form):
		application = form.save()
		message = u'The changes have been saved.'
		messages.success(self.request, message)
		return super(CourseUpdateView, self).form_valid(form)

	def get_success_url(self):
		pk = self.kwargs['pk']
		self.success_url = reverse('courses:edit', kwargs={'pk':pk})
		return self.success_url


class CourseDeleteView(DeleteView):
	model = Course
	template_name = "courses/remove.html"
	context_object_name = "course"
	success_url = reverse_lazy('index')

	def get_context_data(self, **kwargs):
		context = super(CourseDeleteView, self).get_context_data(**kwargs)
		context['title'] = u'Course deletion'		
		return context

	def delete(self, request, *args, **kwargs):		
		message = u'Course %s has been deleted.' % self.get_object().name
		messages.success(self.request, message)
		return super(CourseDeleteView, self).delete(request, *args, **kwargs)


def course_detail(request, id_course):
	lesson = Lesson.objects.filter(course_id=id_course)
	course = Course.objects.get(id=id_course)
	return render(request, 'courses/detail.html', {'course': course, 'lesson':lesson})


def create(request):	
	if request.method == 'POST':
		form = CourseModelForm(request.POST)
		if form.is_valid():
			application = form.save()
			message = u'Course %s has been successfully added.' % (application.name)
			messages.success(request, message)
			return redirect('/')
	else:
		form = CourseModelForm()

	return render(request,'courses/add.html', {'form':form})	


def edit(request, id):
	application = Course.objects.get(id=id)
	if request.method == 'POST':
		form = CourseModelForm(request.POST, instance=application)
		if form.is_valid():
			application = form.save()
			message = u'The changes have been saved.'
			messages.success(request, message)
			return redirect('courses:edit', application.id)			
	else:
		form = CourseModelForm(instance=application)

	return render(request,'courses/edit.html', {'form':form})


def remove(request, id):
	application = Course.objects.get(id=id)
	if request.method == 'POST':
		application.delete()
		message = u'Course %s has been deleted.' % (application.name)
		messages.success(request, message)
		return redirect('/')
	
	return render(request,'courses/remove.html', {'ap':application})


def add_lesson(request, id):	
	if request.method == 'POST':
		form = LessonModelForm(request.POST)
		if form.is_valid():
			application = form.save()
			message = u'Lesson %s has been successfully added.' % (application.subject)
			messages.success(request, message)
			return redirect('courses:detail', application.course.id)
	else:
		course = Course.objects.get(id=id)		
		form = LessonModelForm(initial={'course':course})

	return render(request,'courses/add_lesson.html', {'form':form})

