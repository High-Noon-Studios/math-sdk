"""Game-specific configuration file, inherits from src/config/config.py"""

import os
from src.config.config import Config
from src.config.distributions import Distribution
from src.config.betmode import BetMode
from constants import wincap, rtp, bonus_hunt_cost, regular_bonus_cost, super_bonus_cost

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
        self.paytable = {
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

            (99, "KM"): 0, # only used for symbol registration
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
            "marx": ["KM"],
            "wild": ["W", "KM"],
            "scatter": ["S"],
            "multiplier": ["W"],
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
            self.basegame_type: {2: 120, 3: 30, 4: 20},
            self.freegame_type: {2: 150, 3: 100, 4: 50, 5: 25, 6: 10, 10: 5},
        }
        mult_values_wcap = {
            self.basegame_type: mult_values_default[self.basegame_type],
            self.freegame_type: {10: 1},
        }
        mult_values_super = {
            self.basegame_type: mult_values_default[self.basegame_type],
            self.freegame_type: {4: 150, 6: 100, 8: 50, 10: 25, 12: 10, 20: 5},
        }
        mult_values_super_wcap = {
            self.basegame_type: mult_values_default[self.basegame_type],
            self.freegame_type: {20: 1},
        }

        landing_wilds_default = {
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
        landing_wilds_wcap = {1: 1, 2: 1, 3: 1}

        landing_marx = { 0: 15, 1: 4, 2: 1 }
        # map of "number of wilds on board" to a map of probabilities of number of symbols to be flipped to wilds
        marx_wild_flip = {
            0: {
                0: 3**9,
                1: 3**8,
                2: 3**7,
                3: 3**6,
                4: 3**5,
                5: 3**4,
                6: 3**3,
                7: 3**2,
                8: 3**1,
                9: 3**0
            },
            1: {
                0: 3**9,
                1: 3**8,
                2: 3**7,
                3: 3**6,
                4: 3**5,
                5: 3**4,
                6: 3**3,
                7: 3**2,
                8: 3**1,
            },
            2: {
                0: 3**9,
                1: 3**8,
                2: 3**7,
                3: 3**6,
                4: 3**5,
                5: 3**4,
                6: 3**3,
                7: 3**2,
            },
            3: {
                0: 3**9,
                1: 3**8,
                2: 3**7,
                3: 3**6,
                4: 3**5,
                5: 3**4,
                6: 3**3,
            },
            4: {
                0: 3**9,
                1: 3**8,
                2: 3**7,
                3: 3**6,
                4: 3**5,
                5: 3**4,
            },
            5: {
                0: 3**9,
                1: 3**8,
                2: 3**7,
                3: 3**6,
                4: 3**5,
            },
            6: {
                0: 3**9,
                1: 3**8,
                2: 3**7,
                3: 3**6,
            },
            7: {
                0: 3**9,
                1: 3**8,
                2: 3**7,
            },
            8: {
                0: 3**9,
                1: 3**8,
            },
            9: {
                0: 1,
            }
        }

        marx_mult_increase = {
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
                            "mult_values": mult_values_default,
                            "landing_wilds": landing_wilds_default,
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
                            "mult_values": mult_values_default,
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
                            "reel_weights": {self.basegame_type: {"BR0": 1}},
                            "mult_values": mult_values_default,
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
                            "mult_values": mult_values_wcap,
                            "landing_wilds": landing_wilds_wcap,
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
                            "mult_values": mult_values_default,
                            "landing_wilds": landing_wilds_default,
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
                            "mult_values": mult_values_default,
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
                            "reel_weights": {self.basegame_type: {"BR0": 1}},
                            "mult_values": mult_values_default,
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
                            "mult_values": mult_values_wcap,
                            "landing_wilds": landing_wilds_wcap,
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
                            "mult_values": mult_values_default,
                            "landing_wilds": landing_wilds_default,
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
                            "mult_values": mult_values_super_wcap,
                            "landing_wilds": landing_wilds_wcap,
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
                            "mult_values": mult_values_super,
                            "landing_wilds": landing_wilds_default,
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
