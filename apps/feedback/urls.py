

from django.urls import path
from .views import FeedbackCreateView, FeedbackAdminListView

urlpatterns = [
    path("", FeedbackCreateView.as_view(), name="feedback"),
    path("admin/", FeedbackAdminListView.as_view(), name="admin-feedback"),
]