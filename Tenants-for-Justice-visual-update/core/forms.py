from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User

from .models import Case, Evidence, Incident


class SignUpForm(UserCreationForm):
    email = forms.EmailField(required=True)

    class Meta:
        model = User
        fields = ("username", "email", "password1", "password2")


class CaseForm(forms.ModelForm):
    class Meta:
        model = Case
        fields = ("title", "property_address", "landlord_or_manager", "move_in_date", "summary", "status")
        widgets = {"move_in_date": forms.DateInput(attrs={"type": "date"}), "summary": forms.Textarea(attrs={"rows": 5})}


class IncidentForm(forms.ModelForm):
    class Meta:
        model = Incident
        fields = ("title", "category", "occurred_at", "people_involved", "description")
        widgets = {"occurred_at": forms.DateTimeInput(attrs={"type": "datetime-local"}), "description": forms.Textarea(attrs={"rows": 5})}


class EvidenceForm(forms.ModelForm):
    class Meta:
        model = Evidence
        fields = ("title", "evidence_type", "incident", "file", "notes")
        widgets = {"notes": forms.Textarea(attrs={"rows": 4})}

    def __init__(self, *args, case=None, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields["incident"].queryset = case.incidents.all() if case else Incident.objects.none()
