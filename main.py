
from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.label import Label
from kivy.uix.button import Button
from android import activity
from jnius import autoclass

class WebViewLauncher(BoxLayout):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.orientation = 'vertical'
        self.add_widget(Label(text="Launching PonyXpress WebApp..."))
        self.add_widget(Button(text="Open", on_press=self.launch_browser))

    def launch_browser(self, instance):
        PythonActivity = autoclass('org.kivy.android.PythonActivity')
        Intent = autoclass('android.content.Intent')
        Uri = autoclass('android.net.Uri')
        intent = Intent(Intent.ACTION_VIEW, Uri.parse("http://127.0.0.1:5000"))
        PythonActivity.mActivity.startActivity(intent)

class PonyXpressApp(App):
    def build(self):
        return WebViewLauncher()

if __name__ == "__main__":
    PonyXpressApp().run()
