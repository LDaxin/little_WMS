"""The article detail calendar (§ detail-calendar).

Builds the article's dated terms as one list of items and lays them out on a
month grid: ranges as bars (wrapped per week, stacked in lanes), single days as
dots. Every term is a ``planning.CalendarEntry`` except the expiry date.
"""
import calendar as _calendar
from datetime import date, timedelta

from django.urls import reverse
from django.utils.translation import gettext_lazy as _

# Colour per term kind (occasion / maintenance / lend / borrow / expiry).
TERM_COLORS = {
    "occasion": "#0d6efd",
    "maintenance": "#ffc107",
    "lend": "#0dcaf0",
    "borrow": "#6f42c1",
    "expiry": "#dc3545",
}

TERM_LABELS = {
    "occasion": _("Occasion"),
    "maintenance": _("Maintenance"),
    "lend": _("Lent out"),
    "borrow": _("Borrowed in"),
    "expiry": _("Expiry"),
}


def _kind(entry):
    """The term kind for a calendar entry (loans split into lend/borrow)."""
    if entry.entry_type == "loan":
        loan = getattr(entry, "loan", None)
        return "lend" if (loan and loan.direction == "out") else "borrow"
    return entry.entry_type


def calendar_items(article):
    """The article's dated terms as one list (§ detail-calendar).

    Each item: ``type`` (occasion/maintenance/lend/borrow/expiry), ``title``,
    ``start``, ``end`` (end == start for single-day), ``color``, ``entry``
    (the ``CalendarEntry`` or ``None`` for the expiry date) and an optional
    ``url``.
    """
    from occasion.models import Packlist

    items = []
    for entry in article.calendar_entries.select_related("loan").all():
        kind = _kind(entry)
        items.append({
            "id": "entry-%s" % entry.pk,
            "type": kind,
            "title": entry.title,
            "start": entry.start_date,
            "end": entry.end_date or entry.start_date,
            "color": TERM_COLORS.get(kind, "#6c757d"),
            "entry": entry,
            "url": "",
        })
    for packed in Packlist.objects.filter(article=article).select_related(
        "occasion__calendar_entry"
    ):
        occasion = packed.occasion
        entry = occasion.calendar_entry
        items.append({
            "id": "entry-%s" % entry.pk,
            "type": "occasion",
            "title": entry.title,
            "start": entry.start_date,
            "end": entry.end_date or entry.start_date,
            "color": TERM_COLORS["occasion"],
            "entry": entry,
            "url": reverse("occasion", args=[occasion.pk]),
        })
    if article.ablaufdatum:
        items.append({
            "id": "expiry",
            "type": "expiry",
            "title": _("Expires"),
            "start": article.ablaufdatum,
            "end": article.ablaufdatum,
            "color": TERM_COLORS["expiry"],
            "entry": None,
            "url": "",
        })
    items.sort(key=lambda item: (item["start"], item["title"]))
    return items


def _assign_lanes(segments):
    """Assign each segment the lowest lane that does not overlap (§ detail-calendar)."""
    lanes = []
    for seg in sorted(segments, key=lambda s: (s["col_s"], s["col_e"])):
        for index, lane in enumerate(lanes):
            if all(seg["col_e"] < a or seg["col_s"] > b for a, b in lane):
                lane.append((seg["col_s"], seg["col_e"]))
                seg["lane"] = index
                break
        else:
            lanes.append([(seg["col_s"], seg["col_e"])])
            seg["lane"] = len(lanes) - 1
    return len(lanes)


def month_grid(year, month, items, today=None):
    """Lay the items out on the month's weeks (§ detail-calendar).

    Returns ``{"year", "month", "label", "weeks"}`` where each week is a list of
    7 day cells (``date``, ``day``, ``in_month``, ``is_today``, ``dots``) plus
    ``segments`` (bars with ``left_pct``/``width_pct``/``lane``/continuation
    flags) and ``lane_count``.
    """
    today = today or date.today()
    first = date(year, month, 1)
    last = date(year, month, _calendar.monthrange(year, month)[1])
    start = first - timedelta(days=first.weekday())  # week starts Monday

    weeks = []
    cursor = start
    while cursor <= last:
        cells = []
        for offset in range(7):
            day = cursor + timedelta(days=offset)
            cells.append({
                "date": day,
                "day": day.day,
                "in_month": day.month == month,
                "is_today": day == today,
                "has_term": False,
                "dots": [],
            })
        weeks.append({"cells": cells, "segments": [], "lane_count": 0})
        cursor += timedelta(days=7)

    for item in items:
        begin, end = item["start"], item["end"]
        if end < begin:
            begin, end = end, begin
        if end < start or begin > last:
            continue
        for week in weeks:
            for cell in week["cells"]:
                if begin <= cell["date"] <= end:
                    cell["has_term"] = True
        if begin == end:
            for week in weeks:
                for cell in week["cells"]:
                    if cell["date"] == begin:
                        cell["dots"].append(item)
            continue
        for week in weeks:
            wstart = week["cells"][0]["date"]
            wend = week["cells"][6]["date"]
            if end < wstart or begin > wend:
                continue
            seg_s = max(begin, wstart)
            seg_e = min(end, wend)
            week["segments"].append({
                "item": item,
                "col_s": (seg_s - wstart).days,
                "col_e": (seg_e - wstart).days,
                "continues_left": begin < wstart,
                "continues_right": end > wend,
            })

    for week in weeks:
        week["lane_count"] = _assign_lanes(week["segments"])
        for seg in week["segments"]:
            # dot decimals: the template would otherwise localise the CSS values
            seg["left_pct"] = "%.4f" % (seg["col_s"] / 7 * 100)
            seg["width_pct"] = "%.4f" % ((seg["col_e"] - seg["col_s"] + 1) / 7 * 100)

    return {
        "year": year,
        "month": month,
        "start": first,
        "label": "%s %s" % (_calendar.month_name[month], year),
        "weeks": weeks,
    }


def shift_month(year, month, delta):
    """The (year, month) ``delta`` months away from (year, month) (§ detail-calendar)."""
    total = year * 12 + (month - 1) + delta
    y, m = divmod(total, 12)
    return y, m + 1


def month_strip(year, month, items, today=None):
    """The current month plus its neighbours, newest last (§ detail-calendar)."""
    months = []
    for offset in (-1, 0, 1):
        y, m = shift_month(year, month, offset)
        months.append(month_grid(y, m, items, today=today))
    return months
