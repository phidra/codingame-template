from dataclasses import dataclass

# this line will be replaced by the code merger -> do not reformat them :
# fmt: off
from TOMERGE_logging import info  # noqa
# fmt: on

MAP_WIDTH = 17630
MAP_HEIGHT = 9000


@dataclass
class Board:
    base_x: int = -1
    base_y: int = -1
    my_health: int = -1
    my_mana: int = -1
    enemy_health: int = -1
    enemy_mana: int = -1
    enemy_base_x: int = -1
    enemy_base_y: int = -1

    def __post_init__(self):
        if self.am_I_left():
            info("I am in LEFT corner")
            self.enemy_base_x = MAP_WIDTH
            self.enemy_base_y = MAP_HEIGHT
        else:
            info("I am in RIGHT corner")
            self.enemy_base_x = 0
            self.enemy_base_y = 0

    def am_I_left(self) -> bool:
        return self.base_x == 0 and self.base_y == 0

    def am_I_right(self) -> bool:
        return not self.am_I_left()
