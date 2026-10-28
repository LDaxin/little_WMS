"""Movement buffer state, kept in the user's session (§11).

The buffer holds article codes; the target holds a storage/container code.
The DB-backed ``MovementSession`` groups the audit entries for the session
list and undo.
"""
from django.utils import timezone


def get_open_session(user, create=True):
    """The user's open ``MovementSession`` (§11).

    ``create=False`` only reads (for rendering) and never starts a session.
    """
    from movement.models import MovementSession

    if user is None or not getattr(user, "is_authenticated", False):
        return None
    session = MovementSession.objects.filter(user=user, ended_at=None).first()
    if session is None and create:
        session = MovementSession.objects.create(user=user)
    return session


def end_open_session(user):
    """Close the user's open session (Clear = done, next action starts fresh)."""
    from movement.models import MovementSession

    if user is None or not getattr(user, "is_authenticated", False):
        return
    MovementSession.objects.filter(user=user, ended_at=None).update(ended_at=timezone.now())


def get_state(session):
    state = session.get("movement")
    if not state:
        state = {"mode": "store", "buffer": [], "target": None, "target_smart": False}
        session["movement"] = state
    return state


def save_state(session, state):
    session["movement"] = state
    session.modified = True


def reset(session):
    state = get_state(session)
    state["buffer"] = []
    state["target"] = None
    state["target_smart"] = False
    save_state(session, state)
    return state
