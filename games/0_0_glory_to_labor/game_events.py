"""Events specific to new and updating expanding wild symbols."""

from copy import deepcopy
from src.events.event_constants import EventConstants
from src.events.events import json_ready_sym

NEW_STICKY_SYMS = "newStickySymbols"

def new_sticky_event(gamestate, new_sticky_syms: list):
    """Pass details on new prize symbols"""
    if gamestate.config.include_padding:
        for sym in new_sticky_syms:
            sym["row"] += 1

    event = {"index": len(gamestate.book.events), "type": NEW_STICKY_SYMS, "symbols": new_sticky_syms}
    gamestate.book.add_event(event)