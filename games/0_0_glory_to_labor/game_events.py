"""Events specific to new and updating expanding wild symbols."""

from copy import deepcopy
from src.events.event_constants import EventConstants
from src.events.events import json_ready_sym

NEW_STICKY_SYMS = "newStickySymbols"
FLIP_WILDS = "flipWilds"
INCREASE_WILD_MULT = "increaseWildMult"
MARX_TRIGGER = "marxTrigger"

def marx_trigger(gamestate, positions: list):
    event = {
        "index": len(gamestate.book.events),
        "type": MARX_TRIGGER,
        "positions": positions
    }
    gamestate.book.add_event(event)

def flip_wilds_event(gamestate, symbols_to_flip: list):
    """Pass details on new prize symbols"""
    # Clone symbols_to_flip so the original is not modified
    symbols_to_flip_cloned = deepcopy(symbols_to_flip)
    if gamestate.config.include_padding:
        for sym in symbols_to_flip_cloned:
            sym["row"] += 1

    event = {
        "index": len(gamestate.book.events),
        "type": FLIP_WILDS,
        "symbols": symbols_to_flip_cloned
    }
    gamestate.book.add_event(event)

def increase_wild_mult_event(gamestate, symbols: list):
    symbols_cloned = deepcopy(symbols)
    if gamestate.config.include_padding:
        for sym in symbols_cloned:
            sym["row"] += 1

    """Pass details on new prize symbols"""
    event = {
        "index": len(gamestate.book.events),
        "type": INCREASE_WILD_MULT,
        "symbols": symbols_cloned
    }
    gamestate.book.add_event(event)

def new_sticky_event(gamestate, new_sticky_syms: list):
    """Pass details on new prize symbols"""
    new_sticky_syms_cloned = deepcopy(new_sticky_syms)
    if gamestate.config.include_padding:
        for sym in new_sticky_syms_cloned:
            sym["row"] += 1

    event = {
        "index": len(gamestate.book.events),
        "type": NEW_STICKY_SYMS,
        "symbols": new_sticky_syms_cloned
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

    if (gamestate.gametype == "basegame"):
        # Determine anticipation for basegame: if there is a scatter on both reel 1 and reel 3, set anticipation to 1 on last reel, else 0
        scatter_positions = gamestate.special_syms_on_board.get("scatter", [])
        reels_with_scatter = {pos["reel"] for pos in scatter_positions}
        if 0 in reels_with_scatter and 2 in reels_with_scatter:
            gamestate.anticipation = [0, 0, 0, 0, 1]
        else:
            gamestate.anticipation = [0, 0, 0, 0, 0]

    if (gamestate.gametype == "freegame"):
        marx_positions = gamestate.special_syms_on_board.get("marx", [])
        scatter_positions = gamestate.special_syms_on_board.get("scatter", [])
        reels_with_marx = {pos["reel"] for pos in marx_positions}
        reels_with_scatter = {pos["reel"] for pos in scatter_positions}
        if 0 in reels_with_marx or 0 in reels_with_scatter:
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