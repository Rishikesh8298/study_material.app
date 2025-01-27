from django.shortcuts import render, redirect
from .models import Topic, Subject
from .forms import TopicForm, SubjectForm
from django.contrib import messages


def home(request):
    subject_list = Subject.objects.all().order_by('name')
    return render(request, "home.html", {"subject_list": subject_list})


def add_subject(request):
    if request.method == "POST":
        form = SubjectForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect("add_subject")
        else:
            for field, errors in form.errors.items():
                messages.error(request, f"{field}: {errors}")
                return render(
                    request,
                    "error.html",
                )
    return render(request, "study/subject/add_subject.html")


def edit_subject(request, subject_id):
    subject = Subject.objects.get(id=subject_id)
    if request.method == "POST":
        form = SubjectForm(request.POST, instance=subject)
        if form.is_valid():
            form.save()
            return redirect("home")
    return render(request, "study/subject/edit_subject.html", {"subject": subject})


def add_topic(request):
    if request.method == "POST":
        form = TopicForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect("add_topic")
    else:
        subjects = Subject.objects.all()
        return render(request, "study/topic/add_topic.html", {"subjects": subjects})


def edit_topic(request, topic_id):
    topic = Topic.objects.get(id=topic_id)
    subject = Subject.objects.all().exclude(name=topic.subject.name)
    if request.method == "POST":
        form = TopicForm(request.POST, instance=topic)
        if form.is_valid():
            form.save()
            return redirect("home")
    return render(request, "study/topic/edit_topic.html", {"topic": topic, "subject": subject})


def subject_details(request):
    name = request.GET.get('subject')
    subject = Subject.objects.get(name=name)
    topics = Topic.objects.filter(subject=subject)
    return render(request, "study/subject/subject_details.html", {"subject": subject, "topics": topics})


def topic_details(request):
    name = request.GET.get('topic')
    topic = Topic.objects.get(name=name)
    return render(request, "study/topic/topic_details.html", {"topic": topic})
