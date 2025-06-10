from kivymd.app import MDApp
from kivymd.uix.screen import MDScreen
from kivymd.uix.boxlayout import MDBoxLayout
from kivymd.uix.button import MDRaisedButton, MDFlatButton
from kivymd.uix.label import MDLabel
from kivymd.uix.textfield import MDTextField
from kivymd.uix.scrollview import MDScrollView
from kivy.metrics import dp
from kivymd.uix.screenmanager import MDScreenManager

class RecuperarScreen(MDScreen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)

        scroll = MDScrollView()
        content = MDBoxLayout(
            orientation='vertical',
            padding=[30, 100, 30, 50],
            spacing=24,
            size_hint_y=None
        )
        content.bind(minimum_height=content.setter("height"))

        title = MDLabel(
            text="Recuperar acceso",
            halign="center",
            font_style="H5",
            theme_text_color="Custom",
            text_color=(0.4, 0.2, 0.6, 1),
            size_hint_y=None,
            height=dp(50)
        )

        instruccion = MDLabel(
            text="Te enviaremos un enlace a tu correo electrónico",
            halign="center",
            theme_text_color="Hint",
            size_hint_y=None,
            height=dp(30)
        )

        self.correo = MDTextField(
            hint_text="Correo electrónico",
            icon_right="email-outline",
            mode="rectangle",
            size_hint_x=1
        )

        recuperar_btn = MDRaisedButton(
            text="Enviar instrucciones",
            pos_hint={"center_x": 0.5},
            md_bg_color=(0.4, 0.2, 0.6, 1),
            text_color=(1, 1, 1, 1),
            size_hint=(None, None),
            size=(dp(260), dp(48)),
            elevation=3,
            on_release=self.recuperar
        )

        volver_btn = MDFlatButton(
            text="Volver al inicio",
            pos_hint={"center_x": 0.5},
            text_color=(0.4, 0.2, 0.6, 1),
            size_hint=(None, None),
            size=(dp(200), dp(40)),
            on_release=self.volver
        )

        content.add_widget(title)
        content.add_widget(instruccion)
        content.add_widget(self.correo)
        content.add_widget(recuperar_btn)
        content.add_widget(volver_btn)

        scroll.add_widget(content)
        self.add_widget(scroll)

    def recuperar(self, instance):
        print("Se enviaron las instrucciones al correo.")
        self.manager.current = "login"

    def volver(self, instance):
        self.manager.current = "login"

class TestRecuperarApp(MDApp):
    def build(self):
        sm = MDScreenManager()
        sm.add_widget(RecuperarScreen(name="recuperar"))
        return sm

if __name__ == "__main__":
    TestRecuperarApp().run()
