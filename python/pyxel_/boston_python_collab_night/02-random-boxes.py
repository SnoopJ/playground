import pyxel

SCREEN_WIDTH = 120
SCREEN_HEIGHT = 120

N_BOXES = 25


class App:
    def __init__(self):
        pyxel.init(SCREEN_WIDTH, SCREEN_HEIGHT, title="Hello Pyxel")
        self.boxes = self.generate_boxes(N_BOXES)
        # update and draw()
        pyxel.run(self.update, self.draw)

    def update(self):
        if pyxel.btnp(pyxel.KEY_Q):
            pyxel.quit()
        elif pyxel.btnp(pyxel.KEY_R):
            self.boxes = self.generate_boxes(N_BOXES)

    def draw(self):
        pyxel.cls(0)

        # draw boxes
        for box in self.boxes:
            x, y, w, h, color = box
            pyxel.rect(x, y, w, h, color)

        # NOTE: draw text last so it's on top of any boxes we just drew
        pyxel.text(2, 2, "Press R to regenerate boxes", 7)

    def generate_boxes(
        self,
        N,
        x_min=0,
        x_max=SCREEN_WIDTH,
        y_min=10,
        y_max=SCREEN_HEIGHT,
        w_min=0,
        w_max=20,
        h_min=0,
        h_max=20,
    ):
        boxes = []
        for _ in range(N):
            x = pyxel.rndi(x_min, x_max)
            y = pyxel.rndi(y_min, y_max)
            w = pyxel.rndi(w_min, w_max)
            h = pyxel.rndi(h_min, h_max)
            color = pyxel.rndi(0, 15)  # pyxel has 16 colors
            box = (x, y, w, h, color)
            boxes.append(box)

        return boxes


App()
