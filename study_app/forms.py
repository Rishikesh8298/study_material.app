from .models import Topic, Subject
from django import forms
from django.core.exceptions import ValidationError


class SubjectForm(forms.ModelForm):
    class Meta:
        model = Subject
        fields = ['name', 'description']

    def clean_name(self):
        name = self.cleaned_data.get("name")
        if Subject.objects.filter(name=name).exclude(id=self.instance.id).exists():
            raise ValidationError("Subject name already exists")
        return name


class TopicForm(forms.ModelForm):
    class Meta:
        model = Topic
        fields = ['subject', 'name', 'description']

    def clean_name(self):
        name = self.cleaned_data.get("name")
        if Topic.objects.filter(name=name).exclude(id=self.instance.id).exists():
            raise ValidationError("Topic name already exists")
        return name