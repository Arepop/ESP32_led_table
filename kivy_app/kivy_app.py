from kivy.app import App
from kivy.uix.floatlayout import FloatLayout
from kivy.uix.widget import Widget
from kivy.uix.button import Button
from kivy.uix.colorpicker import ColorWheel, distance, rect_to_polar
from math import pi, sqrt, atan
from kivy.uix.slider import Slider
from colorsys import rgb_to_hsv, hsv_to_rgb
from kivy.uix.spinner import Spinner
from kivy.graphics import Line, Color, InstructionGroup

G_R, G_G, G_B, G_BR = 0, 0, 0, 255
S_D = {1: 1, 2: 1, 3: 1, 4: 1, 5: 1, 6: 1}


def set_command(r, g, b, br):
    print(f'{r}?{g}?{b}?{br}&')


def distance(pt1, pt2):
    return sqrt((pt1[0] - pt2[0]) ** 2. + (pt1[1] - pt2[1]) ** 2.)


class MainScreen(FloatLayout):
    def __init__(self, *args, **kwargs):
        super(MainScreen, self).__init__(*args, **kwargs)


class MyColorWheel(ColorWheel):
    def on__hsv(self, instance, value):
        global G_R
        global G_G
        global G_B
        super(MyColorWheel, self).on__hsv(instance, value)
        G_R, G_G, G_B = (round(self.r * 255),
                         round(self.g * 255), round(self.b * 255))
        set_command(G_R, G_G, G_B, G_BR)

    def on_touch_move(self, touch):
        if touch.grab_current is not self:
            return
        r = self._get_touch_r(touch.pos)
        goal_sv_idx = (touch.ud['orig_sv_idx'] -
                       int((r - touch.ud['anchor_r']) /
                           (float(self._radius) / self._piece_divisions)))

        r, theta = rect_to_polar(self._origin, *touch.pos)
        if r >= self._radius:
            return
        piece = int((theta / (2 * pi)) * self._pieces_of_pie)
        division = int((r / self._radius) * self._piece_divisions)
        self._hsv = self.arcs[self._pieces_of_pie * division + piece].color
        h, s, v, a = self._hsv
        r, g, b = hsv_to_rgb(h, s, v)
        G_R, G_G, G_B = (round(r * 255),
                         round(g * 255), round(b * 255))
        set_command(G_R, G_G, G_B, G_BR)


class MySlider(Slider):
    def on_touch_move(self, touch):
        if self.disabled or not self.collide_point(*touch.pos):
            return
        global G_BR
        super(MySlider, self).on_touch_move(touch)
        if touch.grab_current == self:
            self.value_pos = touch.pos
            G_BR = int(self.value)
        set_command(G_R, G_G, G_B, G_BR)

    def on_touch_down(self, touch):
        global G_BR
        if self.disabled or not self.collide_point(*touch.pos):
            return
        if touch.is_mouse_scrolling:
            if 'down' in touch.button or 'left' in touch.button:
                if self.step:
                    self.value = min(self.max, self.value + self.step)
                else:
                    self.value = min(
                        self.max,
                        self.value + (self.max - self.min) / 20)
            if 'up' in touch.button or 'right' in touch.button:
                if self.step:
                    self.value = max(self.min, self.value - self.step)
                else:
                    self.value = max(
                        self.min,
                        self.value - (self.max - self.min) / 20)
        elif self.sensitivity == 'handle':
            if self.children[0].collide_point(*touch.pos):
                touch.grab(self)
        else:
            touch.grab(self)
            self.value_pos = touch.pos
        G_BR = int(self.value)
        set_command(G_R, G_G, G_B, G_BR)


class MyButton(Button):
    def off(self):
        print('off')

    def on(self):
        print('on')


class MySpinner(Spinner):
    def _on_dropdown_select(self, instance, data, *largs):
        self.text = "Mode"
        self.is_open = False
        self.data = data
        print(self.data)


class MyHexagon(Widget):
    obj_dict = {1: None, 2: None, 3: None, 4: None, 5: None, 6: None}

    def on_touch_down(self, touch):
        if not self.collide_point(*touch.pos):
            return
        angle = self.get_angle(touch)
        if angle > 30 and angle < 90:
            self.side_pick(1)

        elif angle < 30 or angle > 330:
            self.side_pick(2)

        elif angle > 270 and angle < 330:
            self.side_pick(3)

        elif angle < 270 and angle > 210:
            self.side_pick(4)

        elif angle < 210 and angle > 150:
            self.side_pick(5)

        elif angle < 150 and angle > 90:
            self.side_pick(6)

        print(f'{S_D[1]}{S_D[2]}{S_D[3]}{S_D[4]}{S_D[5]}{S_D[6]}')

    def get_angle(self, touch):
        x, y = touch.pos
        xc, yc, = self.li[0], (self.li[1] + self.li[7])/2

        radius, angle = rect_to_polar([xc, yc], x, y)
        angle = int(angle*180/pi)
        return angle

    def side_pick(self, n):
        global S_D
        x, y, q, p = self.li[(2*n-2):n*2+2]
        if self.obj_dict[n] is None:
            self.obj_dict[n] = InstructionGroup()
            self.obj_dict[n].add(Color(1, 1, 0))

            self.obj_dict[n].add(Line(points=[x, y, q, p],
                                      width=4, close=True))
            self.canvas.add(self.obj_dict[n])
            S_D[n] = 1
        else:
            S_D[n] = 0
            self.canvas.remove(self.obj_dict[n])
            self.obj_dict[n] = None

    def on_touch_move(self, touch):
        pass

    def on_touch_up(self, touch):
        pass

    def give_points(self, x, y, h, w):
        if h * 9/16 < w:
            r = h * 9/16
        else:
            r = w
        x1, y1 = x, y + r
        x2, y2 = x + r*0.87, y + 0.5*r
        x3, y3 = x2, y2 - r
        x4, y4 = x, y - r
        x5, y5 = x - 0.87 * r, y - 0.5*r
        x6, y6 = x - 0.87*r, y5 + r
        self.x = x
        self.y = y
        self.r = r
        self.li = [x1, y1, x2, y2, x3, y3, x4, y4, x5, y5, x6, y6, x1, y1]

        return self.li


class KivyAPP(App):
    def build(self):
        root = MainScreen()
        return root


if __name__ == '__main__':
    KivyAPP().run()
