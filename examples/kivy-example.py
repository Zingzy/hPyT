import kivy
from kivy.app import App
from kivy.lang import Builder
from kivy.core.window import Window
Window.clearcolor = (1, 0.5, 0, 0.0)

from hPyT import title_bar_color


root = Builder.load_string('''
Label:
    markup: True
    text:
        ('[b]Hello[/b] [color=94D000]World[/color]\\n'
        '[color=94D000]Hello[/color] [b]World[/b]')
    font_size: '64pt'

''')


class TestApp(App):

    def build(self):
        return root

    def on_start(self):
        
        # window parameter ---> self
        title_bar_color.set(self, "#ff8000")
        
        return super().on_start()


if __name__ == '__main__':
    TestApp().run()
    