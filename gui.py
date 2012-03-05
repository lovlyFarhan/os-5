from kivy.app import App
from kivy.uix.button import Button

class App(App):
    def build(self):
        return Button(text='Real machine')

App().run()
