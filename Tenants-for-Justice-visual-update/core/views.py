from django.contrib.auth import login
from django.contrib.auth.decorators import login_required
from django.shortcuts import get_object_or_404, redirect, render

from .forms import CaseForm, EvidenceForm, IncidentForm, SignUpForm
from .models import Case


def home(request):
    return render(request, "core/home.html")


def signup(request):
    if request.user.is_authenticated:
        return redirect("dashboard")
    form = SignUpForm(request.POST or None)
    if request.method == "POST" and form.is_valid():
        user = form.save()
        login(request, user)
        return redirect("dashboard")
    return render(request, "registration/signup.html", {"form": form})


@login_required
def dashboard(request):
    return render(request, "core/dashboard.html", {"cases": request.user.housing_cases.all()})


@login_required
def case_create(request):
    form = CaseForm(request.POST or None)
    if request.method == "POST" and form.is_valid():
        case = form.save(commit=False)
        case.user = request.user
        case.save()
        return redirect(case)
    return render(request, "core/form.html", {"form": form, "heading": "Start a housing case", "button_text": "Create case"})


def owned_case(request, pk):
    return get_object_or_404(Case, pk=pk, user=request.user)


@login_required
def case_detail(request, pk):
    return render(request, "core/case_detail.html", {"case": owned_case(request, pk)})


@login_required
def case_update(request, pk):
    case = owned_case(request, pk)
    form = CaseForm(request.POST or None, instance=case)
    if request.method == "POST" and form.is_valid():
        form.save()
        return redirect(case)
    return render(request, "core/form.html", {"form": form, "heading": "Edit case", "button_text": "Save changes"})


@login_required
def incident_create(request, pk):
    case = owned_case(request, pk)
    form = IncidentForm(request.POST or None)
    if request.method == "POST" and form.is_valid():
        incident = form.save(commit=False)
        incident.case = case
        incident.save()
        return redirect(case)
    return render(request, "core/form.html", {"form": form, "heading": "Add a timeline event", "button_text": "Save event", "case": case})


@login_required
def evidence_create(request, pk):
    case = owned_case(request, pk)
    form = EvidenceForm(request.POST or None, request.FILES or None, case=case)
    if request.method == "POST" and form.is_valid():
        evidence = form.save(commit=False)
        evidence.case = case
        evidence.save()
        return redirect(case)
    return render(request, "core/form.html", {"form": form, "heading": "Upload evidence", "button_text": "Upload evidence", "case": case, "multipart": True})


def resources(request):
    return render(request, "core/resources.html")


def about(request):
    return render(request, "core/about.html")
