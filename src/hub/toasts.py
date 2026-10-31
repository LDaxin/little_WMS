"""Central toast feedback.

Views render a toast via these helpers instead of building the context dict
(``toastName``/``toastId``/``toastText``/``toastType``) themselves.
"""
from django.shortcuts import render


def toast(request, name, text, type="status", template="hub/modules/toast.html"):
    """Render a toast module with the given name, text, and type."""
    return render(request, template, {
        "toastName": name,
        "toastId": "errorToast" if type == "alert" else "successToast",
        "toastText": text,
        "toastType": type,
    })


def success_toast(request, text, name="Success", template="hub/modules/toast.html"):
    return toast(request, name, text, "status", template)


def error_toast(request, text, name="Error", template="hub/modules/toast.html"):
    return toast(request, name, text, "alert", template)
