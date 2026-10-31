"""Occasion services (§2)."""
from planning.models import CalendarEntry
from planning.services import recurrence_dates
from occasion.models import Occasion, Packlist


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
        for item in occasion.packlist.all():
            Packlist.objects.create(
                occasion=instance, article=item.article, quantity=item.quantity
            )
        created += 1
    return created
