from game_override import GameStateOverride
from src.calculations.lines import Lines
from src.calculations.statistics import get_random_outcome
from src.events.events import update_freespin_event, reveal_event, set_total_event, set_win_event
from game_events import new_sticky_event

class GameState(GameStateOverride):
    """Handles game logic and events for a single simulation number/game-round."""

    def run_spin(self, sim):
        self.reset_seed(sim)
        self.repeat = True
        while self.repeat:
            self.reset_book()
            self.draw_board()

            # Evaluate wins, update wallet, transmit events
            self.evaluate_lines_board()

            self.win_manager.update_gametype_wins(self.gametype)
            if self.check_fs_condition():
                self.run_freespin_from_base()

            self.evaluate_finalwin()
            self.check_repeat()

        self.imprint_wins()

    def run_freespin(self):
        self.reset_fs_spin()
        self.sticky_wilds = []

        criteria = self.criteria
        while self.fs < self.tot_fs and not self.wincap_triggered:
            self.update_freespin()
            self.draw_board(emit_event=False)
            self.replace_wilds_on_board_with_normal_symbols()

            max_num_new_wilds = get_random_outcome(self.get_current_distribution_conditions()["landing_wilds"])
            # if self.betmode == 'bonus' and self.fs == 1:
            #     max_num_new_wilds = get_random_outcome(self.get_current_distribution_conditions()["initial_sticky_wilds"])
            new_sticky_wilds = self.generate_new_sticky_wilds(max_num_new_wilds)
            self.sticky_wilds.extend(new_sticky_wilds)

            self.update_board_with_new_sticky_wilds(new_sticky_wilds)
            reveal_event(self)
            self.update_board_with_existing_sticky_wilds()

            if len(new_sticky_wilds) > 0:
                new_sticky_wilds_with_mults = [
                    {"reel": x["reel"], "row": x["row"], "multiplier": getattr(self.board[x["reel"]][x["row"]], "multiplier", None)}
                    for x in new_sticky_wilds
                ]
                new_sticky_event(self, new_sticky_wilds_with_mults)
                update_freespin_event(self)

            self.evaluate_lines_board()

            if self.check_fs_retrigger_condition():
                self.update_fs_retrigger_amt()

            self.win_manager.update_gametype_wins(self.gametype)

        self.end_freespin()