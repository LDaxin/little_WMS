"""Reports (§33)."""
from datetime import date, timedelta

from django.contrib.auth.decorators import login_required
from django.contrib.contenttypes.models import ContentType
from django.db.models import Count
from django.shortcuts import render

from article.models import Article
from audit.models import AuditLog
from hub.csv import csv_response
from organisation.decorators import require_perm

MOVEMENT_ACTIONS = ["moved", "removed"]


def _range(request):
    """The from/to dates from the query, defaulting to the last 12 months."""
    today = date.today()
    from_str = request.GET.get("from") or (today - timedelta(days=365)).isoformat()
    to_str = request.GET.get("to") or today.isoformat()
    return from_str, to_str


def _movements(request):
    from_str, to_str = _range(request)
    return AuditLog.objects.filter(
        action__in=MOVEMENT_ACTIONS,
        timestamp__date__gte=from_str,
        timestamp__date__lte=to_str,
    )


def _movements_by_month(logs):
    months = {}
    for log in logs:
        key = log.timestamp.strftime("%Y-%m")
        months[key] = months.get(key, 0) + 1
    return sorted(months.items())


def _usage(logs):
    article_ct = ContentType.objects.get_for_model(Article)
    rows = (
        logs.filter(content_type=article_ct)
        .values("object_id")
        .annotate(count=Count("id"))
        .order_by("-count")[:10]
    )
    articles = {a.pk: a for a in Article.objects.filter(pk__in=[r["object_id"] for r in rows])}
    return [{"article": articles.get(r["object_id"]), "count": r["count"]} for r in rows]


def _user_activity(logs):
    return list(
        logs.values("user__username").annotate(count=Count("id")).order_by("-count")
    )


@login_required(login_url='/accounts/login/')
@require_perm("settings.view_all")
def reports(request):
    logs = _movements(request)
    from_str, to_str = _range(request)
    return render(request, "reports/reports.html", {
        "from_date": from_str,
        "to_date": to_str,
        "movements": _movements_by_month(logs),
        "usage": _usage(logs),
        "activity": _user_activity(logs),
    })


@login_required(login_url='/accounts/login/')
@require_perm("settings.view_all")
def reportsExport(request):
    rows = [[month, count] for month, count in _movements_by_month(_movements(request))]
    return csv_response("movements.csv", ["month", "movements"], rows)
