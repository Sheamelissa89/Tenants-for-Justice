from django.urls import path
from . import views

urlpatterns = [
    path("", views.home, name="home"),
    path("signup/", views.signup, name="signup"),
    path("dashboard/", views.dashboard, name="dashboard"),
    path("cases/new/", views.case_create, name="case_create"),
    path("cases/<int:pk>/", views.case_detail, name="case_detail"),
    path("cases/<int:pk>/edit/", views.case_update, name="case_update"),
    path("cases/<int:pk>/events/new/", views.incident_create, name="incident_create"),
    path("cases/<int:pk>/evidence/new/", views.evidence_create, name="evidence_create"),
    path("resources/", views.resources, name="resources"),
    path("about/", views.about, name="about"),
]
