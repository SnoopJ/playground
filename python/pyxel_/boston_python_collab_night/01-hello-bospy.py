import pyxel

SCREEN_WIDTH = 120
SCREEN_HEIGHT = 120


class App:
    def __init__(self):
        pyxel.init(SCREEN_WIDTH, SCREEN_HEIGHT, title="Hello Pyxel")
        # update and draw()
        pyxel.run(self.update, self.draw)

    def update(self):
        if pyxel.btnp(pyxel.KEY_Q):
            pyxel.quit()

    def draw(self):
        pyxel.cls(0)
        pyxel.text(20, 32, "Hello, Boston Python!", pyxel.COLOR_YELLOW)

        # yellow circle
        cx = 60
        cy = 72
        pyxel.circ(x=cx, y=cy, r=25, col=pyxel.COLOR_YELLOW)

        # two black circles (eyes)
        pyxel.circ(x=cx - 10, y=cy - 10, r=3, col=pyxel.COLOR_BLACK)
        pyxel.circ(x=cx + 10, y=cy - 10, r=3, col=pyxel.COLOR_BLACK)

        # three black lines (smile)
        # line(x1, y1, x2, y2, col)
        pyxel.line(x1=cx - 15, y1=cy + 5, x2=cx - 10, y2=cy + 10, col=pyxel.COLOR_BLACK)
        pyxel.line(x1=cx - 10, y1=cy + 10, x2=cx + 10, y2=cy + 10, col=pyxel.COLOR_BLACK)
        pyxel.line(x1=cx + 10, y1=cy + 10, x2=cx + 15, y2=cy + 5, col=pyxel.COLOR_BLACK)


App()
