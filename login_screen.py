from kivymd.uix.screen import MDScreen
from kivymd.uix.scrollview import MDScrollView
from kivymd.uix.boxlayout import MDBoxLayout
from kivymd.uix.button import MDRaisedButton, MDFlatButton, MDFillRoundFlatIconButton
from kivymd.uix.label import MDLabel
from kivymd.uix.textfield import MDTextField
from kivy.uix.anchorlayout import AnchorLayout
from kivy.uix.image import AsyncImage
from kivy.uix.boxlayout import BoxLayout

MORADO = (0.54, 0.17, 0.89, 1)  # Color violeta personalizado
BLANCO = (1, 1, 1, 1)

class LoginScreen(MDScreen):
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

        logo_container = BoxLayout(size_hint_y=None, height=150, padding=(0, 5), orientation='vertical')
        logo = AsyncImage(source='assets/logm.png', size_hint=(None, None), size=(120, 120), allow_stretch=True, pos_hint={"center_x": 0.5})
        logo_container.add_widget(logo)

        subtitle = MDLabel(
            text="Monitorea tu salud fácilmente",
            halign="center",
            theme_text_color="Hint",
            size_hint_y=None,
            height=30
        )

        self.username = MDTextField(
            hint_text="Usuario empresarial",
            icon_right="account-circle",
            mode="rectangle",
            pos_hint={"center_x": 0.5},
            size_hint_x=None,
            width=280
        )
        self.password = MDTextField(
            hint_text="Contraseña",
            password=True,
            icon_right="eye-off",
            mode="rectangle",
            pos_hint={"center_x": 0.5},
            size_hint_x=None,
            width=280
        )

        login_btn_container = BoxLayout(size_hint_y=None, height=70, padding=(72, 5))
        login_btn = MDRaisedButton(
            text="Iniciar sesión",
            md_bg_color=MORADO,
            text_color=BLANCO,
            pos_hint={"center_x": 0},
            on_release=self.login
        )
        login_btn_container.add_widget(login_btn)

        forgot_btn = MDFlatButton(
            text="¿Olvidaste tu contraseña?",
            theme_text_color="Custom",
            text_color=MORADO,
            pos_hint={"center_x": 0.5},
            on_release=self.ir_a_recuperar
        )

        register_btn = MDFlatButton(
            text="Crear nueva cuenta",
            theme_text_color="Custom",
            text_color=MORADO,
            pos_hint={"center_x": 0.5},
            on_release=self.ir_a_registro
        )

        google_btn = MDFillRoundFlatIconButton(
            text="Continuar con Google",
            icon="google",
            pos_hint={"center_x": 0.5},
            text_color=BLANCO,
            md_bg_color=MORADO
        )

        apple_btn = MDFillRoundFlatIconButton(
            text="Continuar con Apple",
            icon="apple",
            pos_hint={"center_x": 0.5},
            text_color=BLANCO,
            md_bg_color=(0.1, 0.1, 0.1, 1)
        )

        content.add_widget(logo_container)
        content.add_widget(subtitle)
        content.add_widget(self.username)
        content.add_widget(self.password)
        content.add_widget(login_btn_container)
        content.add_widget(forgot_btn)
        content.add_widget(register_btn)
        content.add_widget(google_btn)
        content.add_widget(apple_btn)

        anchor.add_widget(content)
        scroll.add_widget(anchor)
        self.add_widget(scroll)

    def login(self, instance):
        if self.username.text == "admin" and self.password.text == "a":
            self.manager.current = "admin"
        else:
            self.manager.current = "ritmo"

    def ir_a_recuperar(self, instance):
        self.manager.current = "recuperar"

    def ir_a_registro(self, instance):
        self.manager.current = "registro"
