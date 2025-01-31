from django.urls import path
from .views import *

urlpatterns = [
    path("", HomeView.as_view(), name="home"),
    path("add-subject/", AddSubjectView.as_view(), name="add_subject"),
    path("edit-subject/<uuid:subject_id>/", EditSubjectView.as_view(), name="edit_subject"),
    path("add-topic/", AddTopicView.as_view(), name="add_topic"),
    path("edit-topic/<uuid:topic_id>/", EditTopicView.as_view(), name="edit_topic"),
    path("subject-details/", SubjectDetailView.as_view(), name="subject_details"),
    path("topic-details/", TopicDetailView.as_view(), name="topic_details"),
    path("apply-filter/", TopicFilterView.as_view(), name="apply_filter"),
]
