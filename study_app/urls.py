from django.urls import path
from .views import *

urlpatterns=  [
    path("", home, name="home"),
    path("add-subject/", add_subject, name="add_subject"),
    path("edit-subject/<uuid:subject_id>/", edit_subject, name="edit_subject"),
    path("add-topic/", add_topic, name="add_topic"),
    path("edit-topic/<uuid:topic_id>/", edit_topic, name="edit_topic"),
    path("subject-details/", subject_details, name="subject_details"),
    path("topic-details/", topic_details, name="topic_details"),
]