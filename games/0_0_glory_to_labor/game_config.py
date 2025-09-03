"""Game-specific configuration file, inherits from src/config/config.py"""

import os
from src.config.config import Config
from src.config.distributions import Distribution
from src.config.betmode import BetMode
from constants import (
    wincap,
    rtp,
    bonus_hunt_cost,
    regular_bonus_cost,
    super_bonus_cost,
    PAYTABLE,
    PAYLINES,
    SPECIAL_SYMBOLS,
    REELS_FILENAMES,
    MULT_VALUES_PRESETS,
    LANDING_WILDS_PRESETS,
    BET_MODE_MULT_VALUES_SELECTIONS,
    BET_MODE_LANDING_WILDS_SELECTIONS,
    LANDING_MARX,
    MARX_WILD_FLIP,
    MARX_MULT_INCREASE,
)

class GameConfig(Config):

    _instance = None

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super().__new__(cls)
        return cls._instance

    def __init__(self):
        super().__init__()
        self.game_id = "0_0_glory_to_labor"
        self.provider_number = 0
        self.working_name = "Glory to Labor!"
        self.wincap = wincap
        self.win_type = "lines"
        self.rtp = rtp
        self.construct_paths()

        self.num_reels = 5
        self.num_rows = [3] * self.num_reels
        self.paytable = PAYTABLE

        self.paylines = PAYLINES

        self.include_padding = True
        self.special_symbols = SPECIAL_SYMBOLS

        self.freespin_triggers = {
            self.basegame_type: {3: 10},
            self.freegame_type: {2: 2},
        }
        self.anticipation_triggers = {
            self.basegame_type: min(self.freespin_triggers[self.basegame_type].keys()) - 1,
            self.freegame_type: min(self.freespin_triggers[self.freegame_type].keys()) - 1,
        }

        reels = REELS_FILENAMES

        self.reels = {}
        for r, f in reels.items():
            self.reels[r] = self.read_reels_csv(
                os.path.join(self.reels_path, f))

        self.padding_reels[self.basegame_type] = self.reels["BR0"]
        self.padding_reels[self.freegame_type] = self.reels["FR0"]

        def map_phase(preset_by_phase):
            return { self.basegame_type: preset_by_phase["base"], self.freegame_type: preset_by_phase["free"] }

        def resolve_mult_values(mode_name: str, criteria: str):
            preset_name = BET_MODE_MULT_VALUES_SELECTIONS[mode_name][criteria]
            return map_phase(MULT_VALUES_PRESETS[preset_name])

        def resolve_landing_wilds(mode_name: str, criteria: str):
            preset_name = BET_MODE_LANDING_WILDS_SELECTIONS[mode_name][criteria]
            return LANDING_WILDS_PRESETS[preset_name]

        landing_marx = LANDING_MARX
        marx_wild_flip = MARX_WILD_FLIP
        marx_mult_increase = MARX_MULT_INCREASE

        self.bet_modes = [
            BetMode(
                name="base",
                cost=1.0,
                rtp=self.rtp,
                max_win=self.wincap,
                auto_close_disabled=False,
                is_feature=True,
                is_buybonus=False,
                distributions=[
                    Distribution(
                        criteria="wincap",
                        quota=0.001,
                        win_criteria=self.wincap,
                        conditions={
                            "reel_weights": {
                                self.basegame_type: {"BR0": 1},
                                self.freegame_type: {"WCAP": 1},
                            },
                            "scatter_triggers": {3: 1},
                            "mult_values": resolve_mult_values("base", "wincap"),
                            "landing_wilds": resolve_landing_wilds("base", "wincap"),
                            "force_wincap": True,
                            "force_freegame": True,
                            "landing_marx": landing_marx,
                            "marx_wild_flip": marx_wild_flip,
                            "marx_mult_increase": marx_mult_increase,
                        },
                    ),
                    Distribution(
                        criteria="freegame",
                        quota=0.12,
                        conditions={
                            "reel_weights": {
                                self.basegame_type: {"BR0": 1},
                                self.freegame_type: {"FR0": 49, "WCAP": 1},
                            },
                            "scatter_triggers": {3: 1},
                            "mult_values": resolve_mult_values("base", "freegame"),
                            "landing_wilds": resolve_landing_wilds("base", "freegame"),
                            "force_wincap": False,
                            "force_freegame": True,
                            "landing_marx": landing_marx,
                            "marx_wild_flip": marx_wild_flip,
                            "marx_mult_increase": marx_mult_increase,
                        },
                    ),
                    Distribution(
                        criteria="0",
                        quota=0.45,
                        win_criteria=0.0,
                        conditions={
                            "reel_weights": {self.basegame_type: {"BR0": 1}},
                            "mult_values": resolve_mult_values("base", "0"),
                            "force_wincap": False,
                            "force_freegame": False,
                            # tease a bonus 1 in 45 spins
                            "scatter_triggers": { 0: 43, 1: 1, 2: 1 },
                            "landing_marx": landing_marx,
                            "marx_wild_flip": marx_wild_flip,
                            "marx_mult_increase": marx_mult_increase,
                        },
                    ),
                    Distribution(
                        criteria="basegame",
                        quota=0.439,
                        conditions={
                            "reel_weights": {self.basegame_type: {"BR0": 99, "BR0_1000x": 1}},
                            "mult_values": resolve_mult_values("base", "basegame"),
                            "force_wincap": False,
                            "force_freegame": False,
                            # tease a bonus 1 in 45 spins
                            "scatter_triggers": { 0: 43, 1: 1, 2: 1 },
                            "landing_marx": landing_marx,
                            "marx_wild_flip": marx_wild_flip,
                            "marx_mult_increase": marx_mult_increase,
                        },
                    ),
                ],
            ),
            BetMode(
                name="bonus_hunt",
                cost=bonus_hunt_cost,
                rtp=self.rtp,
                max_win=self.wincap,
                auto_close_disabled=False,
                is_feature=True,
                is_buybonus=False,
                distributions=[
                    Distribution(
                        criteria="wincap",
                        quota=0.001,
                        win_criteria=self.wincap,
                        conditions={
                            "reel_weights": {
                                self.basegame_type: {"BR0": 1},
                                self.freegame_type: {"WCAP": 1},
                            },
                            "scatter_triggers": {3: 1},
                            "mult_values": resolve_mult_values("bonus_hunt", "wincap"),
                            "landing_wilds": resolve_landing_wilds("bonus_hunt", "wincap"),
                            "force_wincap": True,
                            "force_freegame": True,
                            "landing_marx": landing_marx,
                            "marx_wild_flip": marx_wild_flip,
                            "marx_mult_increase": marx_mult_increase,
                        },
                    ),
                    Distribution(
                        criteria="freegame",
                        quota=0.12,
                        conditions={
                            "reel_weights": {
                                self.basegame_type: {"BR0": 1},
                                self.freegame_type: {"FR0": 49, "WCAP": 1},
                            },
                            "scatter_triggers": {3: 1},
                            "mult_values": resolve_mult_values("bonus_hunt", "freegame"),
                            "landing_wilds": resolve_landing_wilds("bonus_hunt", "freegame"),
                            "force_wincap": False,
                            "force_freegame": True,
                            "landing_marx": landing_marx,
                            "marx_wild_flip": marx_wild_flip,
                            "marx_mult_increase": marx_mult_increase,
                        },
                    ),
                    Distribution(
                        criteria="0",
                        quota=0.45,
                        win_criteria=0.0,
                        conditions={
                            "reel_weights": {self.basegame_type: {"BR0": 1}},
                            "mult_values": resolve_mult_values("bonus_hunt", "0"),
                            "force_wincap": False,
                            "force_freegame": False,
                            # tease a bonus 1 in 9 spins
                            "scatter_triggers": { 0: 7, 1: 1, 2: 1 },
                            "landing_marx": landing_marx,
                            "marx_wild_flip": marx_wild_flip,
                            "marx_mult_increase": marx_mult_increase,
                        },
                    ),
                    Distribution(
                        criteria="basegame",
                        quota=0.439,
                        conditions={
                            "reel_weights": {self.basegame_type: {"BR0": 99, "BR0_1000x": 1}},
                            "mult_values": resolve_mult_values("bonus_hunt", "basegame"),
                            "force_wincap": False,
                            "force_freegame": False,
                            # tease a bonus 1 in 9 spins
                            "scatter_triggers": { 0: 7, 1: 1, 2: 1 },
                            "landing_marx": landing_marx,
                            "marx_wild_flip": marx_wild_flip,
                            "marx_mult_increase": marx_mult_increase,
                        },
                    ),
                ],
            ),
            BetMode(
                name="regular_bonus",
                cost=regular_bonus_cost,
                rtp=self.rtp,
                max_win=self.wincap,
                auto_close_disabled=False,
                is_feature=False,
                is_buybonus=True,
                distributions=[
                    Distribution(
                        criteria="wincap",
                        quota=0.001,
                        win_criteria=self.wincap,
                        conditions={
                            "reel_weights": {
                                self.basegame_type: {"BR0": 1},
                                self.freegame_type: {"WCAP": 1},
                            },
                            "scatter_triggers": {3: 1},
                            "mult_values": resolve_mult_values("regular_bonus", "wincap"),
                            "landing_wilds": resolve_landing_wilds("regular_bonus", "wincap"),
                            "force_wincap": True,
                            "force_freegame": True,
                            "landing_marx": landing_marx,
                            "marx_wild_flip": marx_wild_flip,
                            "marx_mult_increase": marx_mult_increase,
                        },
                    ),
                    Distribution(
                        criteria="freegame",
                        quota=0.999,
                        conditions={
                            "reel_weights": {
                                self.basegame_type: {"BR0": 1},
                                self.freegame_type: {"FR0": 49, "WCAP": 1},
                            },
                            "scatter_triggers": {3: 1},
                            "mult_values": resolve_mult_values("regular_bonus", "freegame"),
                            "landing_wilds": resolve_landing_wilds("regular_bonus", "freegame"),
                            "force_wincap": False,
                            "force_freegame": True,
                            "landing_marx": landing_marx,
                            "marx_wild_flip": marx_wild_flip,
                            "marx_mult_increase": marx_mult_increase,
                        },
                    ),
                ],
            ),
            BetMode(
                name="super_bonus",
                cost=super_bonus_cost,
                rtp=self.rtp,
                max_win=self.wincap,
                auto_close_disabled=False,
                is_feature=False,
                is_buybonus=True,
                distributions=[
                    Distribution(
                        criteria="wincap",
                        quota=0.001,
                        win_criteria=self.wincap,
                        conditions={
                            "reel_weights": {
                                self.basegame_type: {"BR0": 1},
                                self.freegame_type: {"WCAP": 1},
                            },
                            "scatter_triggers": {3: 1},
                            "mult_values": resolve_mult_values("super_bonus", "wincap"),
                            "landing_wilds": resolve_landing_wilds("super_bonus", "wincap"),
                            "force_wincap": True,
                            "force_freegame": True,
                            "landing_marx": landing_marx,
                            "marx_wild_flip": marx_wild_flip,
                            "marx_mult_increase": marx_mult_increase,
                        },
                    ),
                    Distribution(
                        criteria="freegame",
                        quota=0.999,
                        conditions={
                            "reel_weights": {
                                self.basegame_type: {"BR0": 1},
                                self.freegame_type: {"FR0": 49, "WCAP": 1},
                            },
                            "scatter_triggers": {3: 1},
                            "mult_values": resolve_mult_values("super_bonus", "freegame"),
                            "landing_wilds": resolve_landing_wilds("super_bonus", "freegame"),
                            "force_wincap": False,
                            "force_freegame": True,
                            "landing_marx": landing_marx,
                            "marx_wild_flip": marx_wild_flip,
                            "marx_mult_increase": marx_mult_increase,
                        },
                    ),
                ],
            ),
        ]
