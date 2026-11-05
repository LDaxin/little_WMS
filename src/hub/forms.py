from django import forms
from .models import *


def apply_field_classes(form):
    """Give each visible widget a Bootstrap class matching its type.

    Checkboxes get ``form-check-input`` and selects ``form-select`` so they are
    not styled as text inputs (§ detail-view field area).
    """
    for field in form.visible_fields():
        widget = field.field.widget
        input_type = getattr(widget, "input_type", "")
        if input_type == "checkbox":
            widget.attrs["class"] = "form-check-input"
        elif input_type == "select":
            widget.attrs["class"] = "form-select"
        else:
            widget.attrs["class"] = "form-control"

