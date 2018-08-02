from kivy.app import App
from kivy.uix.floatlayout import FloatLayout
from kivy.uix.widget import Widget
from kivy.uix.button import Button
from kivy.uix.colorpicker import ColorWheel
from math import cos, sin, pi, sqrt, atan
from kivy.graphics import Color


class MyColorWheel(ColorWheel):
    def on__hsv(self, instance, value):
        super(MyColorWheel, self).on__hsv(instance, value)
        print(self.rgba)

    def on_touch_move(self, touch):
        super(MyColorWheel, self).on_touch_move(touch)
        r = self._get_touch_r(touch.pos)
        if r > self._radius:
            return False


class KivyAPP(App):
    def build(self):
        return FloatLayout()


if __name__ == '__main__':
    KivyAPP().run()
