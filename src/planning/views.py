"""Calendar view (§2)."""
from django.contrib.auth.decorators import login_required
from django.shortcuts import render

from organisation.decorators import require_perm
from planning.models import CalendarEntry


@login_required(login_url='/accounts/login/')
@require_perm("calendar.view_all")
def calendar(request):
    entries = CalendarEntry.objects.order_by("start_date", "id")
    months = []
    for entry in entries:
        key = entry.start_date.replace(day=1)
        if not months or months[-1][0] != key:
            months.append((key, []))
        months[-1][1].append(entry)
    return render(request, "planning/calendar.html", {"months": months})
