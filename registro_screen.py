from kivymd.app import MDApp
from kivymd.uix.screen import MDScreen
from kivymd.uix.boxlayout import MDBoxLayout
from kivymd.uix.button import MDRaisedButton, MDFlatButton
from kivymd.uix.label import MDLabel
from kivymd.uix.textfield import MDTextField
from kivymd.uix.scrollview import MDScrollView
from kivy.uix.anchorlayout import AnchorLayout
from kivymd.uix.screenmanager import MDScreenManager


class RegistroScreen(MDScreen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)

        scroll = MDScrollView()
        anchor = AnchorLayout(anchor_x='center', anchor_y='top')

        content = MDBoxLayout(
            orientation='vertical',
            padding=30,
            spacing=10,
            size_hint=(None, None),
            width=320
        )
        content.bind(minimum_height=content.setter("height"))

        title = MDLabel(
            text="Crear cuenta",
            halign="center",
            font_style="H5",
            theme_text_color="Primary"
        )

        self.nombre = MDTextField(
            hint_text="Nombre completo",
            icon_right="account",
            pos_hint={"center_x": 0.5},
            size_hint_x=None,
            width=280
        )
        self.email = MDTextField(
            hint_text="Correo electrónico",
            icon_right="email",
            pos_hint={"center_x": 0.5},
            size_hint_x=None,
            width=280
        )
        self.contrasena = MDTextField(
            hint_text="Contraseña",
            password=True,
            icon_right="lock",
            pos_hint={"center_x": 0.5},
            size_hint_x=None,
            width=280
        )
        self.edad = MDTextField(
            hint_text="Edad",
            icon_right="calendar",
            pos_hint={"center_x": 0.5},
            size_hint_x=None,
            width=280
        )
        self.peso = MDTextField(
            hint_text="Peso (kg)",
            icon_right="scale",
            pos_hint={"center_x": 0.5},
            size_hint_x=None,
            width=280
        )
        self.altura = MDTextField(
            hint_text="Altura (cm)",
            icon_right="ruler",
            pos_hint={"center_x": 0.5},
            size_hint_x=None,
            width=280
        )

        registrar_btn = MDRaisedButton(
            text="Registrar",
            md_bg_color=(0.6, 0.4, 0.8, 1),  # morado violeta
            pos_hint={"center_x": 0.5},
            on_release=self.registrar
        )
        volver_btn = MDFlatButton(
            text="Volver al inicio",
            text_color=(0.6, 0.4, 0.8, 1),
            pos_hint={"center_x": 0.5},
            on_release=self.volver
        )

        content.add_widget(title)
        content.add_widget(self.nombre)
        content.add_widget(self.email)
        content.add_widget(self.contrasena)
        content.add_widget(self.edad)
        content.add_widget(self.peso)
        content.add_widget(self.altura)
        content.add_widget(registrar_btn)
        content.add_widget(volver_btn)

        anchor.add_widget(content)
        scroll.add_widget(anchor)
        self.add_widget(scroll)

    def registrar(self, instance):
        print("Registrado:", self.nombre.text, self.email.text)
        self.manager.current = "login"

    def volver(self, instance):
        self.manager.current = "login"


# Solo si ejecutas este archivo directamente
if __name__ == "__main__":
    class TestApp(MDApp):
        def build(self):
            sm = MDScreenManager()
            sm.add_widget(RegistroScreen(name="registro"))
            return sm

    TestApp().run()
