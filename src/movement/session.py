"""Movement buffer state, kept in the user's session (§11).

The buffer holds article codes; the target holds a storage/container code.
"""


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
