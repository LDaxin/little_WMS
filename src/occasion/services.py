"""Occasion services (§2)."""
from datetime import timedelta

from article.models import Article
from planning.models import CalendarEntry
from planning.services import recurrence_dates
from occasion.models import Occasion, Packlist


def packlist_as_list(occasion):
    """The occasion's packlist as a JSON-serialisable list of {article, quantity}.

    This is the single place that knows the packlist shape used by
    ``OccasionTemplate.default_packlist``.
    """
    return [{"article": e.article_id, "quantity": e.quantity} for e in occasion.packlist.all()]


def apply_packlist(occasion, items):
    """Create packlist entries on ``occasion`` from ``{article, quantity}`` items.

    Items whose article no longer exists are skipped.
    """
    for item in items:
        article = Article.objects.filter(pk=item.get("article")).first()
        if article:
            Packlist.objects.create(
                occasion=occasion, article=article, quantity=item.get("quantity") or 1
            )


def copy_packlist(source, target):
    """Copy the packlist of ``source`` onto ``target``."""
    apply_packlist(target, packlist_as_list(source))


def duplicate_occasion(occasion, shift_days=0):
    """Create a copy of an occasion with its packlist, shifting the dates (§2)."""
    head = occasion.calendar_entry
    delta = timedelta(days=shift_days)
    entry = CalendarEntry.objects.create(
        entry_type=head.entry_type,
        title="%s (copy)" % head.title,
        start_date=head.start_date + delta,
        end_date=(head.end_date + delta) if head.end_date else None,
        notes=head.notes,
        responsible_user=head.responsible_user,
    )
    copy = Occasion.objects.create(
        calendar_entry=entry,
        occasion_type=occasion.occasion_type,
        location=occasion.location,
        participant_count=occasion.participant_count,
    )
    copy_packlist(occasion, copy)
    return copy


def repeat_occasion(occasion, rule):
    """Create the future occasions for a recurrence rule (§2).

    Each instance copies the head's type, location, participant count, and
    packlist. Returns the number of instances created.
    """
    head = occasion.calendar_entry
    duration = (head.end_date - head.start_date) if head.end_date else None
    created = 0
    for date in recurrence_dates(head.start_date, rule):
        entry = CalendarEntry.objects.create(
            entry_type=head.entry_type,
            title=head.title,
            start_date=date,
            end_date=(date + duration) if duration else None,
            notes=head.notes,
            responsible_user=head.responsible_user,
            recurrence_rule=rule,
        )
        instance = Occasion.objects.create(
            calendar_entry=entry,
            occasion_type=occasion.occasion_type,
            location=occasion.location,
            participant_count=occasion.participant_count,
        )
        copy_packlist(occasion, instance)
        created += 1
    return created
