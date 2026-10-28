"""Thread-local current organisation (§22).

Set by ``ActiveOrganisationMiddleware``; read by ``OrganisationManager`` and the
``organisation`` field defaults so reads and writes stay within the active org.
"""
import threading

_state = threading.local()


def set_current_organisation(organisation):
    _state.organisation = organisation


def get_current_organisation():
    return getattr(_state, "organisation", None)


def clear_current_organisation():
    _state.organisation = None


def current_organisation_id():
    """Default for the ``organisation`` FK: the active org, else 1."""
    organisation = get_current_organisation()
    return organisation.pk if organisation is not None else 1
