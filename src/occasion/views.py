"""Occasion system (§2): plan material for an event with a packlist."""
from django.utils.translation import gettext as _
from django.contrib.auth.decorators import login_required
from django.db.models import Q
from django.http import HttpResponseNotFound
from django.shortcuts import get_object_or_404, redirect, render

from article.models import Article
from planning.models import CalendarEntry, RecurrenceRule
from location.models import Location
from organisation.decorators import require_perm
from occasion.models import Occasion, OccasionTemplate, OccasionType, Packlist
from occasion.services import duplicate_occasion, repeat_occasion


def _int_or_none(value):
    value = (value or "").strip()
    return int(value) if value.isdigit() else None


def _location(value):
    return Location.objects.filter(pk=value).first() if value else None


def _apply_template(occasion, template):
    """Copy a template's default packlist onto an occasion, skipping gone articles."""
    for item in template.default_packlist:
        article = Article.objects.filter(pk=item.get("article")).first()
        if article:
            Packlist.objects.create(
                occasion=occasion, article=article, quantity=item.get("quantity") or 1
            )


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
        template = OccasionTemplate.objects.filter(pk=request.POST.get("template") or None).first()
        occasion_type = template.occasion_type if template else OccasionType.objects.filter(pk=request.POST.get("type") or None).first()
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
            if template:
                _apply_template(occ, template)
            return redirect("occasion", occasionId=occ.pk)
    return render(request, "occasion/occasionForm.html", {
        "types": OccasionType.objects.all(),
        "templates": OccasionTemplate.objects.all(),
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
@require_perm("occasion.view_all")
def occasionTemplates(request):
    return render(request, "occasion/templates.html", {
        "templates": OccasionTemplate.objects.all(),
        "types": OccasionType.objects.all(),
    })


@login_required(login_url='/accounts/login/')
@require_perm("occasion.create_all")
def addOccasionTemplate(request):
    if request.method == "POST":
        name = request.POST.get("name", "").strip()
        occasion_type = OccasionType.objects.filter(pk=request.POST.get("type") or None).first()
        if name and occasion_type:
            OccasionTemplate.objects.create(name=name, occasion_type=occasion_type)
    return redirect("occasion templates")


@login_required(login_url='/accounts/login/')
@require_perm("occasion.delete_all")
def delOccasionTemplate(request, templateId):
    template = get_object_or_404(OccasionTemplate, pk=templateId)
    if request.method == "POST":
        template.delete()
    return redirect("occasion templates")


@login_required(login_url='/accounts/login/')
@require_perm("occasion.create_all")
def saveOccasionAsTemplate(request, occasionId):
    occ = get_object_or_404(Occasion, pk=occasionId)
    if request.method == "POST":
        OccasionTemplate.objects.create(
            name=request.POST.get("name", "").strip() or str(occ),
            occasion_type=occ.occasion_type,
            default_packlist=[
                {"article": entry.article_id, "quantity": entry.quantity}
                for entry in occ.packlist.all()
            ],
        )
    return redirect("occasion", occasionId=occ.pk)


@login_required(login_url='/accounts/login/')
@require_perm("occasion.edit_all")
def repeatOccasion(request, occasionId):
    occ = get_object_or_404(Occasion, pk=occasionId)
    if request.method == "POST" and occ.calendar_entry.recurrence_rule is None:
        frequency = request.POST.get("frequency")
        if frequency in dict(RecurrenceRule.FREQUENCY_CHOICES):
            rule = RecurrenceRule.objects.create(
                frequency=frequency,
                interval=_int_or_none(request.POST.get("interval")) or 1,
                end_date=request.POST.get("end_date") or None,
                end_after_occurrences=_int_or_none(request.POST.get("end_after_occurrences")),
            )
            occ.calendar_entry.recurrence_rule = rule
            occ.calendar_entry.save()
            repeat_occasion(occ, rule)
    return redirect("occasion", occasionId=occ.pk)


@login_required(login_url='/accounts/login/')
@require_perm("occasion.create_all")
def duplicateOccasion(request, occasionId):
    occ = get_object_or_404(Occasion, pk=occasionId)
    if request.method == "POST":
        shift = _int_or_none(request.POST.get("shift_days")) or 0
        copy = duplicate_occasion(occ, shift)
        return redirect("occasion", occasionId=copy.pk)
    return redirect("occasion", occasionId=occ.pk)


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
def packlistSearch(request, occasionId):
    """Live suggestions for the combined code/name field (§ code-input pattern)."""
    occ = get_object_or_404(Occasion, pk=occasionId)
    query = request.GET.get("code", "").strip()
    if query:
        results = Article.objects.filter(
            Q(base__name__contains=query) | Q(code__code__contains=query)
        )[:20]
    else:
        results = Article.objects.none()
    return render(request, "occasion/packlistResults.html",
                  {"occasion": occ, "results": results})


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


@login_required(login_url='/accounts/login/')
@require_perm("occasion.manage_packlist_all")
def occasionScanner(request, scannerId, state):
    """QR toggle for a code input (shared pattern, see hub/modules/qrScanner.html)."""
    if state == "toggle":
        active = request.POST.get("active_scanner", "")
        if active == scannerId:
            context = {"activeInput": "", "input": scannerId, "state": "off"}
        else:
            context = {"activeInput": active, "input": scannerId, "state": "on", "scan": True}
        return render(request, "hub/modules/toggleScanner.html", context=context)
    return HttpResponseNotFound('<h1>Page not found</h1>')
