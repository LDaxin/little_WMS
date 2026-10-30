"""Occasion system (§2): plan material for an event with a packlist."""
from django.contrib.auth.decorators import login_required
from django.http import HttpResponseNotFound
from django.shortcuts import get_object_or_404, redirect, render

from article.models import Article
from location.models import Location
from organisation.decorators import require_perm
from occasion.models import CalendarEntry, Occasion, OccasionType, Packlist


def _int_or_none(value):
    value = (value or "").strip()
    return int(value) if value.isdigit() else None


def _location(value):
    return Location.objects.filter(pk=value).first() if value else None


def _packlist_context(occasion, error=""):
    return {
        "occasion": occasion,
        "packlist": occasion.packlist.select_related("article__base"),
        "statusChoices": Packlist.STATUS_CHOICES,
        "error": error,
    }


@login_required(login_url='/accounts/login/')
@require_perm("occasion.view_all")
def occasions(request):
    return render(request, "occasion/occasions.html", {"occasions": Occasion.objects.all()})


@login_required(login_url='/accounts/login/')
@require_perm("occasion.view_all")
def occasion(request, occasionId):
    occ = get_object_or_404(Occasion, pk=occasionId)
    return render(request, "occasion/occasion.html", {
        "occasion": occ,
        "locations": Location.objects.all(),
        **_packlist_context(occ),
    })


@login_required(login_url='/accounts/login/')
@require_perm("occasion.create_all")
def addOccasion(request):
    error = ""
    if request.method == "POST":
        occasion_type = OccasionType.objects.filter(pk=request.POST.get("type") or None).first()
        name = request.POST.get("name", "").strip()
        start_date = request.POST.get("start_date", "")
        if occasion_type is None or not name or not start_date:
            error = "Name, type, and start date are required."
        else:
            entry = CalendarEntry.objects.create(
                entry_type="occasion",
                title=name,
                start_date=start_date,
                end_date=request.POST.get("end_date") or None,
                responsible_user=request.user,
            )
            occ = Occasion.objects.create(
                calendar_entry=entry,
                occasion_type=occasion_type,
                location=_location(request.POST.get("location")),
                participant_count=_int_or_none(request.POST.get("participants")),
            )
            return redirect("occasion", occasionId=occ.pk)
    return render(request, "occasion/occasionForm.html", {
        "types": OccasionType.objects.all(),
        "locations": Location.objects.all(),
        "error": error,
    })


@login_required(login_url='/accounts/login/')
@require_perm("occasion.edit_all")
def updateOccasion(request, occasionId):
    occ = get_object_or_404(Occasion, pk=occasionId)
    if request.method == "POST":
        occ.calendar_entry.title = request.POST.get("name", occ.calendar_entry.title).strip()
        occ.calendar_entry.start_date = request.POST.get("start_date") or occ.calendar_entry.start_date
        occ.calendar_entry.end_date = request.POST.get("end_date") or None
        occ.calendar_entry.save()
        occ.participant_count = _int_or_none(request.POST.get("participants"))
        occ.location = _location(request.POST.get("location"))
        occ.save()
    return redirect("occasion", occasionId=occ.pk)


@login_required(login_url='/accounts/login/')
@require_perm("occasion.delete_all")
def delOccasion(request, occasionId):
    occ = get_object_or_404(Occasion, pk=occasionId)
    if request.method == "POST":
        occ.calendar_entry.delete()
        occ.delete()
    return redirect("occasions")


@login_required(login_url='/accounts/login/')
@require_perm("occasion.create_all")
def occasionTypes(request):
    return render(request, "occasion/types.html", {"types": OccasionType.objects.all()})


@login_required(login_url='/accounts/login/')
@require_perm("occasion.create_all")
def addOccasionType(request):
    if request.method == "POST":
        name = request.POST.get("name", "").strip()
        if name:
            OccasionType.objects.create(name=name, symbol=request.POST.get("symbol", "").strip())
    return redirect("occasion types")


@login_required(login_url='/accounts/login/')
@require_perm("occasion.manage_packlist_all")
def packlistAdd(request, occasionId):
    occ = get_object_or_404(Occasion, pk=occasionId)
    error = ""
    if request.method == "POST":
        code = request.POST.get("code", "").strip()
        article = Article.objects.filter(code__code=code).first()
        if article is None:
            error = "No article with code %s" % code
        else:
            Packlist.objects.create(
                occasion=occ, article=article, quantity=_int_or_none(request.POST.get("quantity")) or 1
            )
    return render(request, "occasion/packlist.html", _packlist_context(occ, error))


@login_required(login_url='/accounts/login/')
@require_perm("occasion.manage_packlist_all")
def packlistStatus(request, occasionId, entryId):
    occ = get_object_or_404(Occasion, pk=occasionId)
    entry = get_object_or_404(Packlist, pk=entryId, occasion=occ)
    if request.method == "POST":
        status = request.POST.get("status")
        if status in dict(Packlist.STATUS_CHOICES):
            entry.status = status
            entry.save()
    return render(request, "occasion/packlist.html", _packlist_context(occ))


@login_required(login_url='/accounts/login/')
@require_perm("occasion.manage_packlist_all")
def packlistRemove(request, occasionId, entryId):
    occ = get_object_or_404(Occasion, pk=occasionId)
    entry = get_object_or_404(Packlist, pk=entryId, occasion=occ)
    if request.method == "POST":
        entry.delete()
    return render(request, "occasion/packlist.html", _packlist_context(occ))
