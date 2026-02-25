# from django.urls import path
# from .views import FeedbackCreateView,FeedbackAdminList

# urlpatterns = [
#     path("", FeedbackCreateView.as_view()),

# ]


from django.urls import path
from .views import FeedbackCreateView, FeedbackAdminListView

urlpatterns = [
    path("", FeedbackCreateView.as_view(), name="create-feedback"),
    path("admin/list/", FeedbackAdminListView.as_view(), name="admin-feedback-list"),
]