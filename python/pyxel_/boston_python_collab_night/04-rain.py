from dataclasses import dataclass
import random

import pyxel

SCREEN_WIDTH = 240
SCREEN_HEIGHT = 240

N_POINTS = 6

GRAVITY = 0.1

@dataclass
class Raindrop:
    x: int
    y: int
    vx: float = 0
    vy: float = 0
    col: int = pyxel.COLOR_LIGHT_BLUE
    alive: bool = True

    # _COLORS = [pyxel.COLOR_LIGHT_BLUE, pyxel.COLOR_DARK_BLUE, pyxel.COLOR_CYAN]
    _COLORS = [1, 5, 12]

    def __hash__(self):
        return id(self)

    @classmethod
    def random(cls):
        # worked out the original numbers for 120 so whatever, bodge a scale factor
        VY_SCALE = 5.0
        args = dict(
            x=pyxel.rndi(-10, SCREEN_WIDTH-1),
            y=pyxel.rndi(-10, 0),
            vx=0.05 + pyxel.rndf(-0.2, 2.0),
            vy=pyxel.rndf(VY_SCALE, VY_SCALE + 0.4),
            col=cls._COLORS[pyxel.rndi(0, len(cls._COLORS)-1)]
            # vx=0.0,
            # vy=0.0,
        )
        return cls(**args)

    def draw(self):
        pyxel.rect(self.x, self.y, w=1, h=1, col=self.col)

    def update(self):
        self.x += self.vx
        self.y += self.vy

        self.vy += GRAVITY

        if (self.x > SCREEN_WIDTH or self.x < -50 or
            self.y > SCREEN_HEIGHT):
            self.alive = False


class App:
    def __init__(self):
        pyxel.init(SCREEN_WIDTH, SCREEN_HEIGHT, title="Hello Pyxel")

        self._entities = []
        self._removals = []
        self.paused = True
        print("Paused; press P to unpause")
        # update and draw()
        pyxel.run(self.update, self.draw)

    def update(self):
        if pyxel.btnp(pyxel.KEY_Q):
            pyxel.quit()
        elif pyxel.btnp(pyxel.KEY_P):
            self.paused = not self.paused

        RAIN_RATE = 2

        if not self.paused and pyxel.frame_count % RAIN_RATE == 0:
            num_new = pyxel.rndi(20, 30)
            new_drops = (Raindrop.random() for _ in range(num_new))
            self._entities.extend(new_drops)

        if not self.paused:
            for eid, entity in enumerate(self._entities):
                entity.update()
                if not entity.alive:
                    self._removals.append(eid)

            num_removed = 0
            for eid in self._removals:
                del self._entities[eid-num_removed]
                num_removed += 1

            self._removals.clear()

    def draw(self):
        if self.paused:
            return

        pyxel.cls(0)

        for entity in self._entities:
            entity.draw()

App()