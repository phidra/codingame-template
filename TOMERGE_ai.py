from typing import List

# this line will be replaced by the code merger -> do not reformat them :
# fmt: off
from TOMERGE_game import Board
from TOMERGE_logging import measure_time
# fmt: on

DEFENSE_RADIUS = 6000 + 2200
CONSERVATIVE_DEFENSE_RADIUS = 6000 + 2200
VISIBILITY_RADIUS = 2200


# the decision logic lives here :
@measure_time
def decide_what_to_do(board: Board, current_turn: int, sticky_logs: List[str]) -> None:
    """ Decide what to do, based on the current status of the board.  """

    # strategies are applied sequentially, in priority order
    # each strategy should short-circuit if there is no more action to decide
    high_priority_strategy(board, current_turn, sticky_logs)
    middle_priority_strategy1(board, current_turn, sticky_logs)
    middle_priority_strategy2(board, current_turn, sticky_logs)
    low_priority_strategy(board, current_turn, sticky_logs)

    # we also can post-process what has been decided :
    post_processing(board, current_turn, sticky_logs)


@measure_time
def high_priority_strategy(board: Board, current_turn: int, sticky_logs: List[str]) -> None:
    pass


@measure_time
def middle_priority_strategy1(board: Board, current_turn: int, sticky_logs: List[str]) -> None:
    pass


@measure_time
def middle_priority_strategy2(board: Board, current_turn: int, sticky_logs: List[str]) -> None:
    pass


@measure_time
def low_priority_strategy(board: Board, current_turn: int, sticky_logs: List[str]) -> None:
    pass


@measure_time
def post_processing(board: Board, current_turn: int, sticky_logs: List[str]) -> None:
    pass
