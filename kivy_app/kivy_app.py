from kivy.app import App
from kivy.uix.floatlayout import FloatLayout
from kivy.uix.widget import Widget
from kivy.uix.button import Button
from kivy.uix.colorpicker import ColorWheel, distance, rect_to_polar
from math import pi, sqrt
from kivy.uix.slider import Slider
from colorsys import rgb_to_hsv, hsv_to_rgb
from kivy.uix.spinner import Spinner

G_R, G_G, G_B, G_BR = 0, 0, 0, 255


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
        global G_BR
        super(MySlider, self).on_touch_move(touch)
        if touch.grab_current == self:
            self.value_pos = touch.pos
            G_BR = int(self.value)
        set_command(G_R, G_G, G_B, G_BR)

    def on_touch_down(self, touch):
        global G_BR
        super(MySlider, self).on_touch_down(touch)
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

    def on_touch_down(self, touch):
        pass

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

        return (x1, y1, x2, y2, x3, y3, x4, y4, x5, y5, x6, y6)


class KivyAPP(App):
    def build(self):
        root = MainScreen()
        root.add_widget(MyHexagon())
        return root


if __name__ == '__main__':
    KivyAPP().run()
