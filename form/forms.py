from django.db import models
from django import forms, template
from .models import MentorCertificate

class UniEntryForm(forms.ModelForm):
    certification = forms.ModelMultipleChoiceField(
        required=False,
        queryset=MentorCertificate.objects.all(),
        widget=forms.CheckboxSelectMultiple()
)
