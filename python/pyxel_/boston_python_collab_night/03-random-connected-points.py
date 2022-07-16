from dataclasses import dataclass
from typing import List

import pyxel

SCREEN_WIDTH = 120
SCREEN_HEIGHT = 120

N_POINTS = 6


@dataclass
class Point:
    x: int
    y: int
    connections: List[int]
    vx: float = 0
    vy: float = 0

    def draw(self):
        pyxel.rectb(self.x - 2, self.y - 2, 4, 4, pyxel.COLOR_YELLOW)
        pyxel.rect(self.x - 1, self.y - 1, 2, 2, pyxel.COLOR_GRAY)

    def update(self):
        self.x += self.vx
        self.y += self.vy

        # rudimentary physics: points should bounce when they hit the "edge" of the screen
        if self.x <= 0 or self.x >= SCREEN_WIDTH:
            self.vx *= -1
        if self.y <= 20 or self.y >= SCREEN_HEIGHT:
            self.vy *= -1


class App:
    def __init__(self):
        pyxel.init(SCREEN_WIDTH, SCREEN_HEIGHT, title="Hello Pyxel")
        self.points = self.generate_points(N_POINTS)
        self.paused = True
        # update and draw()
        pyxel.run(self.update, self.draw)

    def update(self):
        if pyxel.btnp(pyxel.KEY_Q):
            pyxel.quit()
        elif pyxel.btnp(pyxel.KEY_P):
            self.paused = not self.paused
        elif pyxel.btnp(pyxel.KEY_R):
            self.points = self.generate_points(N_POINTS)

        if not self.paused:
            for point in self.points:
                point.update()

    def draw(self):
        pyxel.cls(0)

        # draw connections first so they appear underneath points
        for point in self.points:
            for idx in point.connections:
                other = self.points[idx]
                pyxel.line(point.x, point.y, other.x, other.y, pyxel.COLOR_DARK_BLUE)

        # then draw points on top
        for point in self.points:
            point.draw()

        # NOTE: draw text last so it's on top of anything we just drew
        pyxel.text(2, 2, "Press R to regenerate points", 7)
        pyxel.text(2, 12, f"Press P to {'unpause' if self.paused else 'pause'}", 7)

    def generate_points(
        self,
        N,
        x_min=10,
        x_max=SCREEN_WIDTH - 10,
        y_min=20,
        y_max=SCREEN_HEIGHT - 10,
        v_min=0.1,
        v_max=2,
    ):
        pts = []
        for _ in range(N):
            x = pyxel.rndi(x_min, x_max)
            y = pyxel.rndi(y_min, y_max)

            v = pyxel.rndf(v_min, v_max)
            angle = pyxel.rndf(0, 360)
            vx = v*pyxel.cos(angle)
            vy = v*pyxel.sin(angle)

            num_edges = pyxel.rndi(1, 2)
            # NOTE: can connect to self which isn't great
            connections = [pyxel.rndi(0, N - 1) for _ in range(num_edges)]

            pt = Point(x=x, y=y, connections=connections, vx=vx, vy=vy)
            pts.append(pt)

        return pts


App()


from dataclasses import dataclass
from typing import List

import pyxel

SCREEN_WIDTH = 120
SCREEN_HEIGHT = 120

N_POINTS = 6


@dataclass
class Point:
    x: int
    y: int
    connections: List[int]
    vx: float = 0
    vy: float = 0

    def draw(self):
        pyxel.rectb(self.x - 2, self.y - 2, 4, 4, pyxel.COLOR_YELLOW)
        pyxel.rect(self.x - 1, self.y - 1, 2, 2, pyxel.COLOR_GRAY)

    def update(self):
        self.x += self.vx
        self.y += self.vy

        # rudimentary physics: points should bounce when they hit the "edge" of the screen
        if self.x <= 0 or self.x >= SCREEN_WIDTH:
            self.vx *= -1
        if self.y <= 20 or self.y >= SCREEN_HEIGHT:
            self.vy *= -1


class App:
    def __init__(self):
        pyxel.init(SCREEN_WIDTH, SCREEN_HEIGHT, title="Hello Pyxel")
        self.points = self.generate_points(N_POINTS)
        self.paused = True
        # update and draw()
        pyxel.run(self.update, self.draw)

    def update(self):
        if pyxel.btnp(pyxel.KEY_Q):
            pyxel.quit()
        elif pyxel.btnp(pyxel.KEY_P):
            self.paused = not self.paused
        elif pyxel.btnp(pyxel.KEY_R):
            self.points = self.generate_points(N_POINTS)

        if not self.paused:
            for point in self.points:
                point.update()

    def draw(self):
        pyxel.cls(0)

        # draw connections first so they appear underneath points
        for point in self.points:
            for idx in point.connections:
                other = self.points[idx]
                pyxel.line(point.x, point.y, other.x, other.y, pyxel.COLOR_DARK_BLUE)

        # then draw points on top
        for point in self.points:
            point.draw()

        # NOTE: draw text last so it's on top of anything we just drew
        pyxel.text(2, 2, "Press R to regenerate points", 7)
        pyxel.text(2, 12, f"Press P to {'unpause' if self.paused else 'pause'}", 7)

    def generate_points(
        self,
        N,
        x_min=10,
        x_max=SCREEN_WIDTH - 10,
        y_min=20,
        y_max=SCREEN_HEIGHT - 10,
        v_min=0.1,
        v_max=2,
    ):
        pts = []
        for _ in range(N):
            x = pyxel.rndi(x_min, x_max)
            y = pyxel.rndi(y_min, y_max)

            v = pyxel.rndf(v_min, v_max)
            angle = pyxel.rndf(0, 360)
            vx = v*pyxel.cos(angle)
            vy = v*pyxel.sin(angle)

            num_edges = pyxel.rndi(1, 2)
            # NOTE: can connect to self which isn't great
            connections = [pyxel.rndi(0, N - 1) for _ in range(num_edges)]

            pt = Point(x=x, y=y, connections=connections, vx=vx, vy=vy)
            pts.append(pt)

        return pts


App()

from dataclasses import dataclass
from typing import List

import pyxel

SCREEN_WIDTH = 120
SCREEN_HEIGHT = 120

N_POINTS = 6


@dataclass
class Point:
    x: int
    y: int
    connections: List[int]
    vx: float = 0
    vy: float = 0

    def draw(self):
        pyxel.rectb(self.x - 2, self.y - 2, 4, 4, pyxel.COLOR_YELLOW)
        pyxel.rect(self.x - 1, self.y - 1, 2, 2, pyxel.COLOR_GRAY)

    def update(self):
        self.x += self.vx
        self.y += self.vy

        # rudimentary physics: points should bounce when they hit the "edge" of the screen
        if self.x <= 0 or self.x >= SCREEN_WIDTH:
            self.vx *= -1
        if self.y <= 20 or self.y >= SCREEN_HEIGHT:
            self.vy *= -1


class App:
    def __init__(self):
        pyxel.init(SCREEN_WIDTH, SCREEN_HEIGHT, title="Hello Pyxel")
        self.points = self.generate_points(N_POINTS)
        self.paused = True
        # update and draw()
        pyxel.run(self.update, self.draw)

    def update(self):
        if pyxel.btnp(pyxel.KEY_Q):
            pyxel.quit()
        elif pyxel.btnp(pyxel.KEY_P):
            self.paused = not self.paused
        elif pyxel.btnp(pyxel.KEY_R):
            self.points = self.generate_points(N_POINTS)

        if not self.paused:
            for point in self.points:
                point.update()

    def draw(self):
        pyxel.cls(0)

        # draw connections first so they appear underneath points
        for point in self.points:
            for idx in point.connections:
                other = self.points[idx]
                pyxel.line(point.x, point.y, other.x, other.y, pyxel.COLOR_DARK_BLUE)

        # then draw points on top
        for point in self.points:
            point.draw()

        # NOTE: draw text last so it's on top of anything we just drew
        pyxel.text(2, 2, "Press R to regenerate points", 7)
        pyxel.text(2, 12, f"Press P to {'unpause' if self.paused else 'pause'}", 7)

    def generate_points(
        self,
        N,
        x_min=10,
        x_max=SCREEN_WIDTH - 10,
        y_min=20,
        y_max=SCREEN_HEIGHT - 10,
        v_min=0.1,
        v_max=2,
    ):
        pts = []
        for _ in range(N):
            x = pyxel.rndi(x_min, x_max)
            y = pyxel.rndi(y_min, y_max)

            v = pyxel.rndf(v_min, v_max)
            angle = pyxel.rndf(0, 360)
            vx = v*pyxel.cos(angle)
            vy = v*pyxel.sin(angle)

            num_edges = pyxel.rndi(1, 2)
            # NOTE: can connect to self which isn't great
            connections = [pyxel.rndi(0, N - 1) for _ in range(num_edges)]

            pt = Point(x=x, y=y, connections=connections, vx=vx, vy=vy)
            pts.append(pt)

        return pts


App()
