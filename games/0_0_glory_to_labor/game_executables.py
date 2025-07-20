from game_calculations import GameCalculations
from src.calculations.lines import Lines
import random

class GameExecutables(GameCalculations):
    def evaluate_lines_board(self):
        """Populate win-data, record wins, transmit events."""
        self.win_data = Lines.get_lines(self.board, self.config, global_multiplier=self.global_multiplier)
        Lines.record_lines_wins(self)
        self.win_manager.update_spinwin(self.win_data["totalWin"])
        Lines.emit_linewin_events(self)

    def replace_wilds_on_board_with_normal_symbols(self) -> None:
        for reel in self.board:
            for symbol in reel:
                if symbol.name == "W":
                    possible_values = ["L1", "L2", "L3", "L4", "L5", "H1", "H2", "H3", "H4"]
                    symbol.name = random.choice(possible_values)

    def update_board_with_new_sticky_wilds(self, wilds: list[dict]) -> None:
        for sticky_wild in wilds:
            self.board[sticky_wild["reel"]][sticky_wild["row"]] = self.create_symbol("W")

    def update_board_with_existing_sticky_wilds(self) -> None:
        for sticky_wild in self.sticky_wilds:
            self.board[sticky_wild["reel"]][sticky_wild["row"]] = self.create_symbol("W")

    def generate_new_sticky_wilds(self, max_num_new_wilds: int):
        new_sticky_wilds = []
        for _ in range(max_num_new_wilds):
            available_reels = [
                reel_idx
                for reel_idx, reel in enumerate(self.board)
                if not all(sym.name == "W" for sym in reel)
            ]
            if len(available_reels) > 0:
                chosen_reel = random.choice(available_reels)
                available_rows = [
                    row_idx
                    for row_idx in range(self.config.num_rows[chosen_reel])
                    if self.board[chosen_reel][row_idx].name != "W"
                ]
                chosen_row = random.choice(available_rows)

                sticky_wild_details = {"reel": chosen_reel, "row": chosen_row}
                new_sticky_wilds.append(sticky_wild_details)

        return new_sticky_wilds

    # only added this to make the code more readable
    def check_fs_retrigger_condition(self) -> bool:
        return self.check_fs_condition()