from django.shortcuts import render, get_object_or_404
from .forms import TopicForm, SubjectForm
from django.contrib import messages
from django.db.models import Q
from mymodule.pagination import create_pagination
from django.urls import reverse, reverse_lazy
from django.views.generic import TemplateView, UpdateView, DetailView, ListView
from .models import Subject, Topic
from django.views.generic.edit import FormView


class HomeView(TemplateView):
    template_name = "home.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["subject_list"] = Subject.objects.all().order_by('name')
        context["recent_post"] = Topic.objects.all().order_by('-created_at', 'name')[:10]
        return context


class AddSubjectView(FormView):
    template_name = "study/subject/add_subject.html"
    form_class = SubjectForm
    success_url = reverse_lazy("add_subject")

    def form_valid(self, form):
        form.save()
        return super().form_valid(form)

    def form_invalid(self, form):
        for field, errors in form.errors.items():
            messages.error(self.request, f"{field}: {errors}")
        return render(self.request, "error.html")  # Custom error page rendering


class EditSubjectView(UpdateView):
    model = Subject
    form_class = SubjectForm
    template_name = "study/subject/edit_subject.html"

    def get_object(self, queryset=None):
        """Fetch the Subject using subject_id instead of pk."""
        subject_id = self.kwargs.get("subject_id")  # Get subject_id from URL
        return get_object_or_404(Subject, id=subject_id)

    def get_success_url(self):
        """Redirect to subject details with subject name as a query parameter."""
        return f"{reverse('subject_details')}?subject={self.object.name}"

    def form_valid(self, form):
        """Save the form if it's valid."""
        return super().form_valid(form)  # Redirects to `get_success_url`

    def form_invalid(self, form):
        """Handle form errors and render the error template."""
        for field, errors in form.errors.items():
            messages.error(self.request, f"{field}: {errors}")
        return render(self.request, "error.html")  # Custom error page rendering


class SubjectDetailView(DetailView):
    model = Subject
    template_name = "study/subject/subject_details.html"
    context_object_name = "subject"

    def get_object(self, queryset=None):
        """Fetch the Subject using the 'subject' GET parameter instead of pk."""
        subject_name = self.request.GET.get("subject")
        return get_object_or_404(Subject, name=subject_name)

    def get_context_data(self, **kwargs):
        """Add related topics to the context."""
        context = super().get_context_data(**kwargs)
        context["related_contents"] = Topic.objects.filter(subject=self.object)
        return context


class AddTopicView(FormView):
    template_name = "study/topic/add_topic.html"
    form_class = TopicForm
    success_url = reverse_lazy("add_topic")

    def get_context_data(self, **kwargs):
        """Add subjects to the context."""
        context = super().get_context_data(**kwargs)
        context["subjects"] = Subject.objects.all()  # Fetch subjects
        return context

    def form_valid(self, form):
        form.save()
        return super().form_valid(form)

    def form_invalid(self, form):
        for field, errors in form.errors.items():
            messages.error(self.request, f"{field}: {errors}")
        return render(self.request, "error.html")  # Custom error page rendering


class EditTopicView(UpdateView):
    model = Topic
    form_class = TopicForm
    template_name = "study/topic/edit_topic.html"

    def get_object(self, queryset=None):
        """Fetch the Topic using topic_id from the URL."""
        topic_id = self.kwargs.get("topic_id")
        return get_object_or_404(Topic, id=topic_id)

    def get_success_url(self):
        """Redirect to subject details with subject name as a query parameter."""
        return f"{reverse('topic_details')}?topic={self.object.name}"

    def get_context_data(self, **kwargs):
        """Add subjects to the context (excluding the current topic's subject)."""
        context = super().get_context_data(**kwargs)
        topic = self.get_object()
        context["subject"] = Subject.objects.all().exclude(name=topic.subject.name)
        return context

    def form_valid(self, form):
        """Save the form and follow the success URL."""
        form.save()
        return super().form_valid(form)

    def form_invalid(self, form):
        """Handle form errors and render the error template."""
        for field, errors in form.errors.items():
            messages.error(self.request, f"{field}: {errors}")
        return render(self.request, "error.html")  # Custom error page rendering


class TopicDetailView(DetailView):
    model = Topic
    template_name = "study/topic/topic_details.html"
    context_object_name = "topic"  # Custom name for the object

    def get_object(self, queryset=None):
        """Fetch the Topic using the 'topic' GET parameter."""
        topic_name = self.request.GET.get("topic")
        return get_object_or_404(Topic, name=topic_name)

    def get_context_data(self, **kwargs):
        """Add related topics to the context."""
        context = super().get_context_data(**kwargs)
        topic = self.get_object()
        context["related_topic"] = Topic.objects.filter(subject=topic.subject).exclude(name=topic.name)
        return context


class TopicFilterView(ListView):
    model = Topic
    template_name = "study/apply_filter.html"
    context_object_name = "result"
    paginate_by = 13

    def get_queryset(self):
        """Override the default queryset to apply filtering."""
        queryset = Topic.objects.all()
        keyword = self.request.GET.get("key")
        if keyword:
            queryset = queryset.filter(
                Q(name__icontains=keyword) |
                Q(description__icontains=keyword)
            )
        return queryset

    def get_context_data(self, **kwargs):
        """Add recent posts and custom pagination."""
        context = super().get_context_data(**kwargs)
        context["recent_post"] = Topic.objects.all().order_by('-created_at', 'name')[:10]

        # Custom pagination logic (assuming create_pagination is a function you have)
        page = self.request.GET.get("page")
        context["result"] = create_pagination(main=self.get_queryset(), no=self.paginate_by, page=page)
        return context
