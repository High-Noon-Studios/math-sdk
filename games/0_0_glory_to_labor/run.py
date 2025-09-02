"""Main file for generating results for sample lines-pay game."""

import subprocess

from gamestate import GameState
from game_config import GameConfig
from game_optimization import OptimizationSetup
from optimization_program.run_script import OptimizationExecution
from utils.game_analytics.run_analysis import create_stat_sheet
from utils.rgs_verification import execute_all_tests
from src.state.run_sims import create_books
from src.write_data.write_configs import generate_configs

NUM_SIMS = 1e4

if __name__ == "__main__":

    num_threads = 100
    rust_threads = 100
    batching_size = 5000
    compression = True
    profiling = False

    num_sim_args = {
        "base": int(NUM_SIMS),
        "bonus_hunt": int(NUM_SIMS),
        "regular_bonus": int(NUM_SIMS),
        "super_bonus": int(NUM_SIMS),
    }

    run_conditions = {
        "run_sims": True,
        "run_optimization": True,
        "run_analysis": True,
        "run_format_checks": True,
    }
    target_modes = list(num_sim_args.keys())

    config = GameConfig()
    gamestate = GameState(config)
    if run_conditions["run_optimization"] or run_conditions["run_analysis"]:
        optimization_setup_class = OptimizationSetup(config)

    if run_conditions["run_sims"]:
        create_books(
            gamestate,
            config,
            num_sim_args,
            batching_size,
            num_threads,
            compression,
            profiling,
        )

    generate_configs(gamestate)

    if run_conditions["run_optimization"]:
        OptimizationExecution().run_all_modes(config, target_modes, rust_threads)
        generate_configs(gamestate)

    if run_conditions["run_analysis"]:
        custom_keys = [{"symbol": "scatter"}]
        create_stat_sheet(gamestate, custom_keys=custom_keys)

    if run_conditions["run_format_checks"]:
        execute_all_tests(config)

    try:
        subprocess.run(
            ["node", "sync-math-to-web.js", "0_0_glory_to_labor"],
            check=True,
            cwd="../utils"
        )
    except Exception as e:
        print(f"Failed to run sync-math-to-web.js: {e}")

    try:
        subprocess.run(
            ["make", "visualize", "GAME=0_0_glory_to_labor"],
            check=True,
        )
    except Exception as e:
        print(f"Failed to run visualize: {e}")