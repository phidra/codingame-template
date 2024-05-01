from typing import List
from dataclasses import dataclass, field
import datetime

# this line will be replaced by the code merger -> do not reformat them :
# fmt: off
from TOMERGE_logging import info, fatal, perflog, DISABLE_PERFLOG, measure_time, measure_time_ctx
from TOMERGE_ai import decide_what_to_do
from TOMERGE_board import Board
# fmt: on


@dataclass
class Game:
    sticky_logs: List[str] = field(default_factory=list)
    board: Board = field(default_factory=Board)
    current_turn: int = 0

    def __post_init__(self) -> None:
        # read game initialization inputs :
        base_x, base_y = [int(i) for i in input().split()]
        info(f"My base is in {base_x}x{base_y}")
        self.board = Board(base_x=base_x, base_y=base_y)

    @measure_time
    def parse_new_turn(self, board: Board) -> None:
        """ Mutates board with new infos received from codingame referee. """

        with measure_time_ctx("reading turn inputs"):
            info(f"++++++++++++++++++++ NEW TURN {self.current_turn} ++++++++++++++++++++")
            self.current_turn += 1

            # WARNING : first turn might take very long (probably the time for the game engine to compute next turn) :
            with measure_time_ctx("reading turn's first input"):
                board.my_health, board.my_mana = [int(j) for j in input().split()]
            board.enemy_health, board.enemy_mana = [int(j) for j in input().split()]

    def print_actions(self, board: Board) -> None:
        print("TODO")
        fatal("fatal")

    def main_loop(self) -> None:
        TURN_TIME_WARNING = 45
        TURN_TIME_ALERT = 50

        while True:
            before = datetime.datetime.now()
            self.do_one_loop()
            after = datetime.datetime.now()
            turn_time = int((after - before).total_seconds() * 1000)
            perflog(f"TURN {self.current_turn} = {turn_time} ms")

            if not DISABLE_PERFLOG:
                if turn_time >= TURN_TIME_WARNING and turn_time < TURN_TIME_ALERT:
                    msg = f"TURN {self.current_turn} time warning = {turn_time} ms"
                    self.sticky_logs.append(msg)
                if turn_time >= TURN_TIME_ALERT:
                    msg = f"TURN {self.current_turn} time ALERT = {turn_time} ms"
                    self.sticky_logs.append(msg)

    def do_one_loop(self) -> None:
        self.parse_new_turn(self.board)
        decide_what_to_do(self.board, self.current_turn, self.sticky_logs)
        self.print_actions(self.board)

        # sticky logging :
        for log in self.sticky_logs:
            info(log)
