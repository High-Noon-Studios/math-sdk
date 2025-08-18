"""Set conditions/parameters for optimization program program"""

from constants import wincap, free_game_hr, wincap_from_base_game_hr, wincap_from_regular_bonus_hr, wincap_from_super_bonus_hr

from optimization_program.optimization_config import (
    ConstructScaling,
    ConstructParameters,
    ConstructConditions,
    verify_optimization_input,
)


class OptimizationSetup:
    def __init__(self, game_config):
        self.game_config = game_config
        self.game_config.opt_params = {
            "base": {
                "conditions": {
                    "wincap": ConstructConditions(rtp=0.01, hr=wincap_from_base_game_hr, av_win=wincap, search_conditions=wincap).return_dict(),
                    "0": ConstructConditions(rtp=0, av_win=0, search_conditions=0).return_dict(),
                    "freegame": ConstructConditions(
                        rtp=0.45, hr=free_game_hr, search_conditions={"symbol": "scatter"}
                    ).return_dict(),
                    "basegame": ConstructConditions(hr=4, rtp=0.505).return_dict(),
                },
                "scaling": ConstructScaling(
                    [
                        {"criteria": "freegame", "scale_factor": 5.0, "win_range": (0, 0.2), "probability": 1.0},
                        {"criteria": "freegame", "scale_factor": 0.2, "win_range": (0.2, 5), "probability": 1.0},
                    ]
                ).return_dict(),
                "parameters": ConstructParameters(
                    num_show=5000,
                    num_per_fence=10000,
                    min_m2m=4,
                    max_m2m=8,
                    pmb_rtp=1.0,
                    sim_trials=5000,
                    test_spins=[50, 100, 200],
                    test_weights=[0.3, 0.4, 0.3],
                    score_type="rtp",
                ).return_dict(),
            },
            "regular_bonus": {
                "conditions": {
                    "wincap": ConstructConditions(rtp=0.01, av_win=wincap, hr=wincap_from_regular_bonus_hr, search_conditions=wincap).return_dict(),
                    "0": ConstructConditions(rtp=0, av_win=0, search_conditions=0).return_dict(),
                    "freegame": ConstructConditions(rtp=0.955, hr="x").return_dict(),
                },
                "scaling": ConstructScaling(
                    [
                        {"criteria": "freegame", "scale_factor": 5.0, "win_range": (0, 20), "probability": 1.0},
                        {"criteria": "freegame", "scale_factor": 0.2, "win_range": (20, 500), "probability": 1.0},
                    ]
                ).return_dict(),
                "parameters": ConstructParameters(
                    num_show=5000,
                    num_per_fence=10000,
                    min_m2m=10,
                    max_m2m=20,
                    pmb_rtp=1.0,
                    sim_trials=5000,
                    test_spins=[10, 20, 50],
                    test_weights=[0.6, 0.2, 0.2],
                    score_type="rtp",
                ).return_dict(),
            },
            "super_bonus": {
                "conditions": {
                    "wincap": ConstructConditions(rtp=0.01, av_win=wincap, hr=wincap_from_super_bonus_hr, search_conditions=wincap).return_dict(),
                    "0": ConstructConditions(rtp=0, av_win=0, search_conditions=0).return_dict(),
                    "freegame": ConstructConditions(rtp=0.955, hr="x").return_dict(),
                },
                "scaling": ConstructScaling(
                    [
                        {"criteria": "freegame", "scale_factor": 5.0, "win_range": (0, 20), "probability": 1.0},
                        {"criteria": "freegame", "scale_factor": 0.2, "win_range": (20, 500), "probability": 1.0},
                    ]
                ).return_dict(),
                "parameters": ConstructParameters(
                    num_show=5000,
                    num_per_fence=10000,
                    min_m2m=10,
                    max_m2m=20,
                    pmb_rtp=1.0,
                    sim_trials=5000,
                    test_spins=[10, 20, 50],
                    test_weights=[0.6, 0.2, 0.2],
                    score_type="rtp",
                ).return_dict(),
            },
            # "super_bonus": {
            #     "conditions": {
            #         "wincap": ConstructConditions(0.01, av_win=wincap, hr=wincap_from_super_bonus_hr, search_conditions=wincap).return_dict(),
            #         "0": ConstructConditions(rtp=0, av_win=0, search_conditions=0).return_dict(),
            #         "freegame": ConstructConditions(rtp=0.955, hr="x").return_dict(),
            #     },
            #     "scaling": ConstructScaling(
            #         [
            #         #    {"criteria": "freegame", "scale_factor": 4.0, "win_range": (0, 40), "probability": 1.0},
            #         #    {"criteria": "freegame", "scale_factor": 0.25, "win_range": (40, 1000), "probability": 1.0},
            #         ]
            #     ).return_dict(),
            #     "parameters": ConstructParameters(
            #         num_show=5000,
            #         num_per_fence=10000,
            #         min_m2m=10,
            #         max_m2m=20,
            #         pmb_rtp=1.0,
            #         sim_trials=5000,
            #         test_spins=[10, 20, 50],
            #         test_weights=[0.6, 0.2, 0.2],
            #         score_type="rtp",
            #     ).return_dict(),
            # },
        }

        verify_optimization_input(self.game_config, self.game_config.opt_params)
