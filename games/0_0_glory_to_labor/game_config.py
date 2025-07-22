"""Game-specific configuration file, inherits from src/config/config.py"""

import os
from src.config.config import Config
from src.config.distributions import Distribution
from src.config.betmode import BetMode


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
        self.wincap = 6750.0
        self.win_type = "lines"
        self.rtp = 0.965
        self.construct_paths()

        self.num_reels = 5
        self.num_rows = [3] * self.num_reels
        self.paytable = {
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
        }

        self.paylines = {
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

        self.include_padding = True
        self.special_symbols = {
            "wild": ["W"],
            "scatter": ["S"],
            "multiplier": ["W"]
        }

        self.freespin_triggers = {
            self.basegame_type: {3: 10},
            self.freegame_type: {2: 2},
        }
        self.anticipation_triggers = {
            self.basegame_type: min(self.freespin_triggers[self.basegame_type].keys()) - 1,
            self.freegame_type: min(self.freespin_triggers[self.freegame_type].keys()) - 1,
        }

        reels = {
            "BR0": "BR0.csv",
            "FR0": "FR0.csv",
            "WCAP": "WCAP.csv"
        }

        self.reels = {}
        for r, f in reels.items():
            self.reels[r] = self.read_reels_csv(
                os.path.join(self.reels_path, f))

        self.padding_reels[self.basegame_type] = self.reels["BR0"]
        self.padding_reels[self.freegame_type] = self.reels["FR0"]

        mult_values_default = {
            self.basegame_type: {1: 120, 2: 30, 3: 20},
            self.freegame_type: {1: 100, 2: 35, 3: 25},
        }
        mult_values_2x = {
            self.basegame_type: mult_values_default[self.basegame_type],
            self.freegame_type: {2: 100, 4: 35, 6: 25},
        }
        mult_values_2x_wcap = {
            self.basegame_type: mult_values_default[self.basegame_type],
            self.freegame_type: {6: 1},
        }
        mult_values_3x = {
            self.basegame_type: mult_values_default[self.basegame_type],
            self.freegame_type: {3: 100, 6: 35, 9: 25},
        }
        mult_values_3x_wcap = {
            self.basegame_type: mult_values_default[self.basegame_type],
            self.freegame_type: {8: 1},
        }
        mult_values_4x = {
            self.basegame_type: mult_values_default[self.basegame_type],
            self.freegame_type: {4: 100, 8: 35, 12: 25},
        }
        mult_values_4x_wcap = {
            self.basegame_type: mult_values_default[self.basegame_type],
            self.freegame_type: {10: 1},
        }
        mult_values_wcap = {
            self.basegame_type: mult_values_default[self.basegame_type],
            self.freegame_type: {3: 1},
        }

        landing_wilds_default = {0: 200, 1: 20, 2: 10, 3: 1}
        landing_wilds_wcap = {1: 1, 2: 1, 3: 1}

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
                            "mult_values": mult_values_wcap,
                            "landing_wilds": landing_wilds_wcap,
                            "force_wincap": True,
                            "force_freegame": True,
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
                            "mult_values": mult_values_default,
                            "landing_wilds": landing_wilds_default,
                            "force_wincap": False,
                            "force_freegame": True,
                        },
                    ),
                    Distribution(
                        criteria="0",
                        quota=0.45,
                        win_criteria=0.0,
                        conditions={
                            "reel_weights": {self.basegame_type: {"BR0": 1}},
                            "mult_values": mult_values_default,
                            "force_wincap": False,
                            "force_freegame": False,
                        },
                    ),
                    Distribution(
                        criteria="basegame",
                        quota=0.439,
                        conditions={
                            "reel_weights": {self.basegame_type: {"BR0": 1}},
                            "mult_values": mult_values_default,
                            "force_wincap": False,
                            "force_freegame": False,
                        },
                    ),
                ],
            ),
            BetMode(
                name="bonus_2x",
                cost=20.0,
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
                            "mult_values": mult_values_2x_wcap,
                            "landing_wilds": landing_wilds_wcap,
                            "force_wincap": True,
                            "force_freegame": True,
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
                            "mult_values": mult_values_2x,
                            "landing_wilds": landing_wilds_default,
                            "force_wincap": False,
                            "force_freegame": True,
                        },
                    ),
                ],
            ),
            BetMode(
                name="bonus_3x",
                cost=40.0,
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
                            "mult_values": mult_values_3x_wcap,
                            "landing_wilds": landing_wilds_wcap,
                            "force_wincap": True,
                            "force_freegame": True,
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
                            "mult_values": mult_values_3x,
                            "landing_wilds": landing_wilds_default,
                            "force_wincap": False,
                            "force_freegame": True,
                        },
                    ),
                ],
            ),
            BetMode(
                name="bonus_4x",
                cost=60.0,
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
                            "mult_values": mult_values_4x_wcap,
                            "landing_wilds": landing_wilds_wcap,
                            "force_wincap": True,
                            "force_freegame": True,
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
                            "mult_values": mult_values_4x,
                            "landing_wilds": landing_wilds_default,
                            "force_wincap": False,
                            "force_freegame": True,
                        },
                    ),
                ],
            ),
        ]
