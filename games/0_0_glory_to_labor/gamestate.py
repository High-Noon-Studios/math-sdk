from game_override import GameStateOverride
from src.calculations.lines import Lines
from src.calculations.statistics import get_random_outcome
from src.events.events import update_freespin_event, set_total_event, set_win_event
from game_events import new_sticky_event, reveal_event, flip_wilds_event, increase_wild_mult_event, marx_trigger
import random

class GameState(GameStateOverride):
    """Handles game logic and events for a single simulation number/game-round."""

    def run_spin(self, sim):
        self.reset_seed(sim)
        self.repeat = True
        while self.repeat:
            self.reset_book()
            self.draw_board(emit_event=False)

            if (self.check_fs_condition()):
                self.anticipation = [0, 0, 0, 0, 1]

            reveal_event(self)

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

            if (self.check_fs_retrigger_condition()):
                self.anticipation = [0, 0, 0, 0, 1]

            self.replace_wilds_on_board_with_normal_symbols()

            marx_symbols_count = get_random_outcome(self.get_current_distribution_conditions()["landing_marx"])
            if (marx_symbols_count > 0):
                self.anticipation = [0, 0, 0, 0, 1]

                if (marx_symbols_count == 1):
                    self.board[0][random.choice(range(self.config.num_rows[0]))] = self.create_symbol("KM")
                if (marx_symbols_count == 2):
                    self.board[0][random.choice(range(self.config.num_rows[0]))] = self.create_symbol("KM")
                    self.board[4][random.choice(range(self.config.num_rows[4]))] = self.create_symbol("KM")

            max_num_new_wilds = get_random_outcome(self.get_current_distribution_conditions()["landing_wilds"])
            # guarantee at least one sticky wild on the first free spin
            if (self.fs == 1 and max_num_new_wilds == 0):
                max_num_new_wilds = 1
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

            if (marx_symbols_count == 2):
                marx_trigger(self)
                wilds_on_board = self.get_wilds_on_board()
                num_wilds_on_board = len(wilds_on_board)
                marx_wild_flip_count = get_random_outcome(self.get_current_distribution_conditions()["marx_wild_flip"][num_wilds_on_board])

                if (marx_wild_flip_count > 0):
                    symbols_to_flip = [
                        {"reel": x["reel"], "row": x["row"], "multiplier": 1}
                        for x in self.generate_new_sticky_wilds(marx_wild_flip_count)
                    ]
                    self.update_board_with_new_sticky_wilds(symbols_to_flip)
                    flip_wilds_event(self, symbols_to_flip)

                updated_sticky_wilds = []
                for r, c in wilds_on_board:
                    marx_mult_increase = get_random_outcome(self.get_current_distribution_conditions()["marx_mult_increase"])
                    if (marx_mult_increase > 0):
                        self.board[r][c].multiplier += marx_mult_increase
                        self.sticky_wilds = [
                            x if x["row"] != r or x["reel"] != c else {"reel": x["reel"], "row": x["row"], "multiplier": x["multiplier"] + marx_mult_increase}
                            for x in self.sticky_wilds
                        ]
                        updated_sticky_wilds.append({"reel": r, "row": c, "multiplier": self.board[r][c].multiplier})

                if (len(updated_sticky_wilds) > 0):
                    increase_wild_mult_event(self, updated_sticky_wilds)

            self.evaluate_lines_board()

            if self.check_fs_retrigger_condition():
                self.update_fs_retrigger_amt()

            self.win_manager.update_gametype_wins(self.gametype)

        self.end_freespin()