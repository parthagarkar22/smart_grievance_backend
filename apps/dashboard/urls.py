from django.urls import path
from .views.citizen import CitizenDashboardView
from .views.officer import OfficerDashboardView
from .views.admin import AdminDashboardView
from apps.dashboard.views.officer import OfficerDashboardView
from apps.dashboard.views.admin import AdminDashboardView



urlpatterns = [
    path("citizen/", CitizenDashboardView.as_view()),
    path("officer/", OfficerDashboardView.as_view()),
    path("admin/", AdminDashboardView.as_view()),
   path("officer/", OfficerDashboardView.as_view(), name="officer-dashboard"), #add changes
     path("admin/", AdminDashboardView.as_view(), name="admin-dashboard"),


]


