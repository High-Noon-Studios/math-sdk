from game_calculations import GameCalculations
from src.calculations.lines import Lines
import random
from src.calculations.statistics import get_random_outcome

class GameExecutables(GameCalculations):
    def draw_board(self, emit_event: bool = True, trigger_symbol: str = "scatter") -> None:
        """Instead of retrying to draw a board, force the initial revel to have a
        specific number of scatters, if the betmode criteria specifies this."""
        if (
            self.get_current_distribution_conditions()["force_freegame"]
            and self.gametype == self.config.basegame_type
        ):
            num_scatters = get_random_outcome(self.get_current_distribution_conditions()["scatter_triggers"])
            self.force_special_board(trigger_symbol, num_scatters)
        elif (
            not (self.get_current_distribution_conditions()["force_freegame"])
            and self.gametype == self.config.basegame_type
        ):
            self.create_board_reelstrips()
            # allows us to control the "tease rate" for scatters in the base game
            num_scatters = get_random_outcome(self.get_current_distribution_conditions()["scatter_triggers"])
            while self.count_special_symbols(trigger_symbol) != num_scatters:
                self.create_board_reelstrips()
        else:
            self.create_board_reelstrips()
        if emit_event:
            reveal_event(self)

    def evaluate_lines_board(self):
        """Populate win-data, record wins, transmit events."""
        self.win_data = Lines.get_lines(self.board, self.config, global_multiplier=self.global_multiplier)
        Lines.record_lines_wins(self)
        self.win_manager.update_spinwin(self.win_data["totalWin"])
        Lines.emit_linewin_events(self)

    def replace_wilds_on_board_with_normal_symbols(self) -> None:
        for reel_idx, reel in enumerate(self.board):
            for row_idx, symbol in enumerate(reel):
                if symbol.name == "W":
                    possible_values = ["L1", "L2", "L3", "L4", "L5", "H1", "H2", "H3", "H4"]
                    new_symbol = self.create_symbol(random.choice(possible_values))
                    self.board[reel_idx][row_idx] = new_symbol

    def update_board_with_new_sticky_wilds(self, wilds: list[dict]) -> None:
        for sticky_wild in wilds:
            self.board[sticky_wild["reel"]][sticky_wild["row"]] = self.create_symbol("W")
            self.board[sticky_wild["reel"]][sticky_wild["row"]].assign_attribute({"multiplier": sticky_wild["multiplier"]})

    def update_board_with_existing_sticky_wilds(self) -> None:
        for sticky_wild in self.sticky_wilds:
            self.board[sticky_wild["reel"]][sticky_wild["row"]] = self.create_symbol("W")
            self.board[sticky_wild["reel"]][sticky_wild["row"]].assign_attribute({"multiplier": sticky_wild["multiplier"]})

    def generate_new_sticky_wilds(self, max_num_new_wilds: int):
        new_sticky_wilds = []

        for _ in range(max_num_new_wilds):
            all_sticky_wilds = self.sticky_wilds + new_sticky_wilds
            # wilds can only appear on reels 2, 3, and 4
            candidate_reel_indexes = [1, 2, 3]
            # Determine which reels (2, 3, 4) have at least one available row (not already occupied by a sticky wild)
            available_reels = []
            for reel_idx in candidate_reel_indexes:
                # Get all rows for this reel
                total_rows = self.config.num_rows[reel_idx]
                # Find which rows are already occupied by sticky wilds
                occupied_rows = {w["row"] for w in all_sticky_wilds if w["reel"] == reel_idx}
                # If there is at least one unoccupied row, this reel is available
                if len(occupied_rows) < total_rows:
                    available_reels.append(reel_idx)

            if len(available_reels) > 0:
                chosen_reel = random.choice(available_reels)
                available_rows = [
                    row_idx
                    for row_idx in range(self.config.num_rows[chosen_reel])
                    if not any(w["reel"] == chosen_reel and w["row"] == row_idx for w in all_sticky_wilds)
                ]
                chosen_row = random.choice(available_rows)

                sticky_wild_details = {"reel": chosen_reel, "row": chosen_row, "multiplier": get_random_outcome(
                    self.get_current_distribution_conditions()["mult_values"][self.gametype]
                )}
                new_sticky_wilds.append(sticky_wild_details)

        return new_sticky_wilds

    # only added this to make the code more readable
    def check_fs_retrigger_condition(self) -> bool:
        return self.check_fs_condition()

    def check_marx_trigger_condition(self) -> bool:
        if self.count_symbols_on_board("KM") >= 2 and not (self.repeat):
            return True
        return False