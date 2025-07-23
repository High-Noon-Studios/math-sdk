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

    event = {
        "index": len(gamestate.book.events),
        "type": NEW_STICKY_SYMS,
        "symbols": new_sticky_syms
    }
    gamestate.book.add_event(event)

def reveal_event(gamestate):
    """Display the initial board drawn from reelstrips."""
    board_client = []
    special_attributes = list(gamestate.config.special_symbols.keys())
    for reel, _ in enumerate(gamestate.board):
        board_client.append([])
        for row in range(len(gamestate.board[reel])):
            board_client[reel].append(json_ready_sym(gamestate.board[reel][row], special_attributes))

    if gamestate.config.include_padding:
        for reel, _ in enumerate(board_client):
            board_client[reel] = [json_ready_sym(gamestate.top_symbols[reel], special_attributes)] + board_client[
                reel
            ]
            board_client[reel].append(json_ready_sym(gamestate.bottom_symbols[reel], special_attributes))

    if (gamestate.check_fs_condition()):
        gamestate.anticipation = [0, 0, 0, 0, 1]
    else:
        gamestate.anticipation = [0, 0, 0, 0, 0]

    event = {
        "index": len(gamestate.book.events),
        "type": EventConstants.REVEAL.value,
        "board": board_client,
        "paddingPositions": gamestate.reel_positions,
        "gameType": gamestate.gametype,
        "anticipation": gamestate.anticipation,
    }
    gamestate.book.add_event(event)