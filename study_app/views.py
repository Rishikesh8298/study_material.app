from django.shortcuts import render, redirect
from .models import Topic, Subject
from .forms import TopicForm, SubjectForm
from django.contrib import messages


def home(request):
    subject_list = Subject.objects.all().order_by('name')
    recent_post = Topic.objects.all().order_by('-created_at', 'name')[:10]
    return render(request, "home.html", {"subject_list": subject_list, "recent_post": recent_post})


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

def subject_details(request):
    name = request.GET.get('subject')
    subject = Subject.objects.get(name=name)
    related_contents = Topic.objects.filter(subject=subject)
    return render(request, "study/subject/subject_details.html", {"subject": subject, "related_contents": related_contents})



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




def topic_details(request):
    name = request.GET.get('topic')
    topic = Topic.objects.get(name=name)
    related_topic = Topic.objects.filter(subject=topic.subject).exclude(name=topic.name)
    return render(request, "study/topic/topic_details.html", {"topic": topic, "related_topic": related_topic})
