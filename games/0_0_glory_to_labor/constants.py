rtp = 0.965
wincap = 10000.0
bonus_hunt_cost = 3.0
regular_bonus_cost = 100.0
super_bonus_cost = 200.0

base_game_hr = 4 # 1 in 4 spins should return something to the player
free_game_hr = 180 # 1 in 180 spins should trigger a free game
bonus_hunt_free_game_hr = free_game_hr / 5 # 5x more likely to trigger a free game
wincap_from_base_game_hr = 5000000 # 1 in 5,000,000 spins should trigger a win cap
wincap_from_regular_bonus_hr = 25_000 # 1 in 25,000 spins should trigger a win cap
wincap_from_super_bonus_hr = 10_000 # 1 in 10,000 spins should trigger a win cap
wincap_from_base_game_rtp = wincap / wincap_from_base_game_hr
wincap_from_regular_bonus_rtp = (wincap / regular_bonus_cost) / wincap_from_regular_bonus_hr
wincap_from_super_bonus_rtp = (wincap / super_bonus_cost) / wincap_from_super_bonus_hr

# -----------------------------
# Centralized configurable presets
# -----------------------------

PAYTABLE = {
    (5, "W"): 8,
    (4, "W"): 2,

    (5, "H1"): 8,
    (4, "H1"): 2,
    (3, "H1"): 0.8,

    (5, "H2"): 6,
    (4, "H2"): 1.5,
    (3, "H2"): 0.6,

    (5, "H3"): 4,
    (4, "H3"): 1.0,
    (3, "H3"): 0.4,

    (5, "H4"): 4.0,
    (4, "H4"): 0.8,
    (3, "H4"): 0.4,

    (5, "L1"): 1.2,
    (4, "L1"): 0.4,
    (3, "L1"): 0.3,

    (5, "L2"): 1,
    (4, "L2"): 0.7,
    (3, "L2"): 0.3,

    (5, "L3"): 0.5,
    (4, "L3"): 0.3,
    (3, "L3"): 0.1,

    (5, "L4"): 0.5,
    (4, "L4"): 0.2,
    (3, "L4"): 0.1,

    (5, "L5"): 0.5,
    (4, "L5"): 0.2,
    (3, "L5"): 0.1,

    (99, "KM"): 0,
}

PAYLINES = {
    1: [0, 0, 0, 0, 0],
    2: [1, 1, 1, 1, 1],
    3: [2, 2, 2, 2, 2],
    4: [0, 1, 2, 1, 0],
    5: [2, 1, 0, 1, 2],
    6: [1, 0, 0, 0, 1],
    7: [1, 2, 2, 2, 1],
    8: [0, 0, 1, 2, 2],
    9: [2, 2, 1, 0, 0],
    10: [1, 2, 1, 0, 1],
    11: [1, 0, 1, 2, 1],
    12: [0, 1, 1, 1, 0],
    13: [2, 1, 1, 1, 2],
    14: [0, 1, 0, 1, 0],
    15: [2, 1, 2, 1, 2],
    16: [1, 1, 0, 1, 1],
    17: [1, 1, 2, 1, 1],
    18: [0, 0, 2, 0, 0],
    19: [2, 2, 0, 2, 2],
    20: [0, 2, 2, 2, 0],
}

SPECIAL_SYMBOLS = {
    "marx": ["KM"],
    "wild": ["W", "KM"],
    "scatter": ["S"],
    "multiplier": ["W"],
}

REELS_FILENAMES = {
    "BR0": "BR0.csv",
    "BR0_1000x": "BR0_1000x.csv",
    "FR0": "FR0.csv",
    "WCAP": "WCAP.csv",
}

MULT_VALUES_DEFAULT_BY_PHASE = {
    "base": {2: 120, 3: 30, 4: 20},
    "free": {2: 150, 3: 100, 4: 50, 5: 25, 6: 10, 10: 5},
}
MULT_VALUES_WCAP_BY_PHASE = {
    "base": MULT_VALUES_DEFAULT_BY_PHASE["base"],
    "free": {10: 1},
}
MULT_VALUES_SUPER_BY_PHASE = {
    "base": MULT_VALUES_DEFAULT_BY_PHASE["base"],
    "free": {4: 150, 6: 100, 8: 50, 10: 25, 12: 10, 20: 5},
}
MULT_VALUES_SUPER_WCAP_BY_PHASE = {
    "base": MULT_VALUES_DEFAULT_BY_PHASE["base"],
    "free": {20: 1},
}

LANDING_WILDS_DEFAULT = {
    0: 5**9,
    1: 5**8,
    2: 5**7,
    3: 5**6,
    4: 5**5,
    5: 5**4,
    6: 5**3,
    7: 5**2,
    8: 5**1,
    9: 5**0,
}
LANDING_WILDS_WCAP = {1: 1, 2: 1, 3: 1}

LANDING_MARX = {0: 15, 1: 4, 2: 1}
MARX_WILD_FLIP = {
    0: {0: 3**9, 1: 3**8, 2: 3**7, 3: 3**6, 4: 3**5, 5: 3**4, 6: 3**3, 7: 3**2, 8: 3**1, 9: 3**0},
    1: {0: 3**9, 1: 3**8, 2: 3**7, 3: 3**6, 4: 3**5, 5: 3**4, 6: 3**3, 7: 3**2, 8: 3**1},
    2: {0: 3**9, 1: 3**8, 2: 3**7, 3: 3**6, 4: 3**5, 5: 3**4, 6: 3**3, 7: 3**2},
    3: {0: 3**9, 1: 3**8, 2: 3**7, 3: 3**6, 4: 3**5, 5: 3**4, 6: 3**3},
    4: {0: 3**9, 1: 3**8, 2: 3**7, 3: 3**6, 4: 3**5, 5: 3**4},
    5: {0: 3**9, 1: 3**8, 2: 3**7, 3: 3**6, 4: 3**5},
    6: {0: 3**9, 1: 3**8, 2: 3**7, 3: 3**6},
    7: {0: 3**9, 1: 3**8, 2: 3**7},
    8: {0: 3**9, 1: 3**8},
    9: {0: 1},
}
MARX_MULT_INCREASE = {
    0: 3**10,
    1: 3**9,
    2: 3**8,
    3: 3**7,
    4: 3**6,
    5: 3**5,
    6: 3**4,
    7: 3**3,
    8: 3**2,
    9: 3**1,
    10: 3**0,
}

MULT_VALUES_PRESETS = {
    "default": MULT_VALUES_DEFAULT_BY_PHASE,
    "wcap": MULT_VALUES_WCAP_BY_PHASE,
    "super": MULT_VALUES_SUPER_BY_PHASE,
    "super_wcap": MULT_VALUES_SUPER_WCAP_BY_PHASE,
}
LANDING_WILDS_PRESETS = {
    "default": LANDING_WILDS_DEFAULT,
    "wcap": LANDING_WILDS_WCAP,
}

BET_MODE_MULT_VALUES_SELECTIONS = {
    "base": {"wincap": "wcap", "freegame": "default", "0": "default", "basegame": "default"},
    "bonus_hunt": {"wincap": "wcap", "freegame": "default", "0": "default", "basegame": "default"},
    "regular_bonus": {"wincap": "wcap", "freegame": "default"},
    "super_bonus": {"wincap": "super_wcap", "freegame": "super"},
}

BET_MODE_LANDING_WILDS_SELECTIONS = {
    "base": {"wincap": "wcap", "freegame": "default", "0": "default", "basegame": "default"},
    "bonus_hunt": {"wincap": "wcap", "freegame": "default", "0": "default", "basegame": "default"},
    "regular_bonus": {"wincap": "wcap", "freegame": "default"},
    "super_bonus": {"wincap": "wcap", "freegame": "default"},
}