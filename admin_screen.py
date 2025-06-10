from kivymd.uix.screen import MDScreen
from kivymd.uix.boxlayout import MDBoxLayout
from kivymd.uix.button import MDRaisedButton, MDFlatButton, MDIconButton
from kivymd.uix.label import MDLabel
from kivymd.uix.card import MDCard
from kivymd.uix.dialog import MDDialog
from kivymd.uix.list import MDList, OneLineIconListItem, IconLeftWidget
from kivymd.uix.scrollview import MDScrollView
from kivy.uix.image import Image
from kivy.uix.anchorlayout import AnchorLayout
from kivy.uix.floatlayout import FloatLayout
from kivy.graphics import Color, Rectangle
from kivy.uix.scrollview import ScrollView
from kivy.uix.widget import Widget
from kivymd.uix.menu import MDDropdownMenu
from kivymd.uix.textfield import MDTextField
from kivymd.app import MDApp
from kivymd.uix.screenmanager import MDScreenManager

class AdminScreen(MDScreen):
    def __init__(self, **kwargs):
        self.usuarios = kwargs.pop("usuarios", [])  # <- MUY IMPORTANTE que esté ANTES del super
        super().__init__(**kwargs)
          
        self.main_layout = MDBoxLayout(orientation='vertical')
        self._crear_toolbar()
        self.scroll = MDScrollView()
        self.content = MDBoxLayout(orientation='vertical', spacing=16, padding=16, size_hint_y=None)
        self.content.bind(minimum_height=self.content.setter("height"))

        self._crear_resumen()
        self._crear_botones_accion()
        self._crear_lista_usuarios()

        self.scroll.add_widget(self.content)
        self.main_layout.add_widget(self.scroll)
        self.add_widget(self.main_layout)

    def _crear_toolbar(self):
        toolbar = MDBoxLayout(orientation='horizontal', size_hint_y=None, height=70, padding=[10, 0, 10, 0])
        with toolbar.canvas.before:
            self.gradient_rects = []
            num_strips = 100
            color1 = (138/255, 43/255, 226/255)
            color2 = (59/255, 2/255, 190/255)
            for i in range(num_strips):
                t = i / (num_strips - 1)
                r = color1[0] * (1 - t) + color2[0] * t
                g = color1[1] * (1 - t) + color2[1] * t
                b = color1[2] * (1 - t) + color2[2] * t
                Color(r, g, b, 1)
                rect = Rectangle()
                self.gradient_rects.append(rect)

        def update_gradient(instance, value):
            if hasattr(self, 'gradient_rects'):
                toolbar_width = instance.size[0]
                strip_width = toolbar_width / len(self.gradient_rects)
                for i, rect in enumerate(self.gradient_rects):
                    rect.pos = (instance.pos[0] + i * strip_width, instance.pos[1])
                    rect.size = (strip_width, instance.size[1])
        toolbar.bind(pos=update_gradient, size=update_gradient)

        title_label = MDLabel(text="Panel\nAdministrativo", font_style="Caption", theme_text_color="Custom", text_color=(1, 1, 1, 1), halign="left", valign="middle", size_hint_x=0.33)
        logo_center = AnchorLayout(anchor_x='center', anchor_y='center', size_hint_x=0.34)
        logo = Image(source="assets/logb.png", size_hint=(None, None), size=(100, 100), allow_stretch=True, keep_ratio=True)
        logo_center.add_widget(logo)

        logout_btn_box = FloatLayout(size_hint_x=0.33)
        logout_btn = MDIconButton(icon="logout", theme_text_color="Custom", text_color=(1, 1, 1, 1), on_release=self.logout, pos_hint={"right": 1, "center_y": 0.5})
        logout_btn_box.add_widget(logout_btn)

        toolbar.add_widget(title_label)
        toolbar.add_widget(logo_center)
        toolbar.add_widget(logout_btn_box)
        self.main_layout.add_widget(toolbar)

    def _crear_resumen(self):
        total = len(self.usuarios)
        activos = len([u for u in self.usuarios if u["estado"] == "Activo"])
        alertas = sum(1 for u in self.usuarios if any(r < 60 or r > 100 for r in u["ritmo_cardiaco"]))

        card = MDCard(orientation='vertical', padding=16, size_hint_y=None, adaptive_height=True, elevation=2, radius=[8])
        title = MDLabel(text="Resumen del Sistema", font_style="H6", size_hint_y=None, height=40)
        grid = MDBoxLayout(orientation='horizontal', size_hint_y=None, height=100)

        grid.add_widget(self._crear_stat(total, "Usuarios", (0.6, 0.4, 0.8, 1)))
        grid.add_widget(self._crear_stat(activos, "Activos", (0.2, 0.7, 0.3, 1)))
        grid.add_widget(self._crear_stat(alertas, "Alertas", (0.9, 0.3, 0.3, 1)))

        card.add_widget(title)
        card.add_widget(grid)
        self.content.add_widget(card)

    def _crear_stat(self, valor, texto, color):
        box = MDBoxLayout(orientation='vertical', padding=8)
        box.add_widget(MDLabel(text=str(valor), halign="center", font_style="H4", theme_text_color="Custom", text_color=color))
        box.add_widget(MDLabel(text=texto, halign="center", theme_text_color="Secondary"))
        return box

    def _crear_botones_accion(self):
        box = MDBoxLayout(orientation='horizontal', size_hint_y=None, height=80, spacing=8)

        add_btn = MDRaisedButton(text="Agregar Usuario", size_hint=(1, None), height=60, md_bg_color=(89/255, 38/255, 209/255), on_release=self.abrir_dialogo_agregar)
        report_btn = MDRaisedButton(text="Generar Reportes", size_hint=(1, None), height=60, md_bg_color=(89/255, 38/255, 209/255), on_release=self.ir_a_reportes)

        box.add_widget(add_btn)
        box.add_widget(report_btn)
        self.content.add_widget(box)

    def ir_a_reportes(self, instance):
        self.manager.current = "reportes"

    def _crear_lista_usuarios(self):
        self.users_title = MDLabel(text="Usuarios Recientes", font_style="H6", size_hint_y=None, height=50)
        self.users_list = MDList()
        for user in self.usuarios:
            icon = "account-check" if user["estado"] == "Activo" else "account-alert"
            color = (0.2, 0.7, 0.3, 1) if user["estado"] == "Activo" else (0.9, 0.3, 0.3, 1)
            item = OneLineIconListItem(text=f"{user['nombre']} - {user['estado']}", on_release=lambda x, u=user: self.ver_detalles_usuario(u))
            item.add_widget(IconLeftWidget(icon=icon, theme_text_color="Custom", text_color=color))
            self.users_list.add_widget(item)

        self.content.add_widget(self.users_title)
        self.content.add_widget(self.users_list)

    def ver_detalles_usuario(self, user):
        layout = MDBoxLayout(orientation="vertical", spacing=12, padding=10, adaptive_height=True)

        def crear_tarjeta(titulo, campos):
            card = MDCard(orientation="vertical", padding=30, spacing=50, adaptive_height=True, size_hint_y=None, elevation=2)
            card.add_widget(MDLabel(text=titulo, font_style="Subtitle1", theme_text_color="Primary"))
            for campo in campos:
                card.add_widget(MDLabel(text=campo, theme_text_color="Secondary"))
            return card

        layout.add_widget(crear_tarjeta("📋 Información Personal", [
            f"Nombre: {user['nombre']}",
            f"Edad: {user['edad']} años",
            f"Peso: {user['peso']} kg",
            f"Altura: {user['altura']} cm",
            f"Correo: {user['correo']}",
            f"Estado: {user['estado']}"
        ]))

        layout.add_widget(crear_tarjeta(" Salud", [
            f"Enfermedades: {user['enfermedades']}",
            f"Medicamentos: {user['medicamentos']}",
            f"Alergias: {user['alergias']}",
            f"Grupo sanguíneo: {user['grupo_sanguineo']}",
            f"Contacto emergencia: {user['contacto_emergencia']}"
        ]))

        grafico = "".join(self._barras_de_bpm(bpm) for bpm in user["ritmo_cardiaco"])
        ritmo = [f"{bpm} bpm - {'⚠️ ALTA' if bpm > 100 else '⚠️ BAJA' if bpm < 60 else '✅ Normal'}" for bpm in user["ritmo_cardiaco"]]
        ritmo.append("\n📊 Gráfico simulado:")
        ritmo.append(grafico)

        layout.add_widget(crear_tarjeta("📈 Ritmo cardíaco", ritmo))

        scroll = ScrollView(size_hint=(1, None), size=(360, 650))
        scroll.add_widget(layout)

        self.detalles_dialog = MDDialog(
            title="Detalles del Usuario",
            type="custom",
            content_cls=scroll,
            buttons=[
                MDFlatButton(text="Eliminar", text_color=(1, 0, 0, 1), on_release=lambda x: self.eliminar_usuario(user)),
                MDFlatButton(text="Cerrar", on_release=lambda x: self.detalles_dialog.dismiss())
            ],
            size_hint=(0.95, None),
            height=700
        )
        self.detalles_dialog.open()

    def _barras_de_bpm(self, bpm):
        if bpm < 60: return "▁"
        elif bpm < 70: return "▂"
        elif bpm < 80: return "▃"
        elif bpm < 90: return "▄"
        elif bpm < 100: return "▅"
        elif bpm < 110: return "▆"
        elif bpm < 120: return "▇"
        else: return "█"

    def eliminar_usuario(self, user):
        self.usuarios.remove(user)
        self.detalles_dialog.dismiss()
        self._actualizar_pantalla()

    def _actualizar_pantalla(self):
        self.content.clear_widgets()
        self._crear_resumen()
        self._crear_botones_accion()
        self._crear_lista_usuarios()

    def abrir_dialogo_agregar(self, instance):
        # Campos normales
        self.nombre_field = MDTextField(hint_text="Nombre completo", size_hint_y=None, height=50)
        self.edad_field = MDTextField(hint_text="Edad", input_filter="int", size_hint_y=None, height=50)
        self.peso_field = MDTextField(hint_text="Peso (kg)", input_filter="int", size_hint_y=None, height=50)
        self.altura_field = MDTextField(hint_text="Altura (cm)", input_filter="int", size_hint_y=None, height=50)
        self.correo_field = MDTextField(hint_text="Correo electrónico", size_hint_y=None, height=50)
        self.enfermedades_field = MDTextField(hint_text="Enfermedades previas", size_hint_y=None, height=50)
        self.medicamentos_field = MDTextField(hint_text="Medicamentos actuales", size_hint_y=None, height=50)
        self.contacto_field = MDTextField(hint_text="Contacto de emergencia", size_hint_y=None, height=50)
        self.alergias_field = MDTextField(hint_text="Alergias", size_hint_y=None, height=50)

        # Dropdown de Estado
        self.estado_field = MDTextField(
            hint_text="Estado",
            text="Activo",
            size_hint_y=None,
            height=50,
            readonly=True,
            icon_right="menu-down"
        )
        self.estado_field.bind(on_touch_down=self.mostrar_estado_dropdown)

        estados = ["Activo", "Inactivo"]
        self.menu_estado = MDDropdownMenu(
            caller=self.estado_field,
            items=[{"text": estado, "on_release": lambda x=estado: self.seleccionar_estado(x)} for estado in estados],
            width_mult=2.5
        )

        # Dropdown de grupo sanguíneo
        self.grupo_field = MDTextField(
            hint_text="Grupo sanguíneo",
            text="O+",
            size_hint_y=None,
            height=50,
            readonly=True,
            icon_right="menu-down"
        )
        self.grupo_field.bind(on_touch_down=self.mostrar_grupo_dropdown)

        grupos = ["A+", "A-", "B+", "B-", "AB+", "AB-", "O+", "O-"]
        self.menu_grupo = MDDropdownMenu(
            caller=self.grupo_field,
            items=[{"text": g, "on_release": lambda x=g: self.seleccionar_grupo(x)} for g in grupos],
            width_mult=2.5
        )

        # Armar el layout
        fields = [
            self.nombre_field, self.edad_field, self.peso_field, self.altura_field, self.estado_field,
            self.correo_field, self.enfermedades_field, self.medicamentos_field,
            self.contacto_field, self.grupo_field, self.alergias_field
        ]

        layout = MDBoxLayout(orientation="vertical", spacing=10, padding=10, adaptive_height=True)
        for field in fields:
            layout.add_widget(field)

        scroll = ScrollView(size_hint=(1, None), size=(360, 400))
        scroll.add_widget(layout)

        self.dialogo_agregar = MDDialog(
            title="Agregar Usuario",
            type="custom",
            content_cls=scroll,
            buttons=[
                MDFlatButton(text="Cancelar", on_release=lambda x: self.dialogo_agregar.dismiss()),
                MDFlatButton(text="Agregar", on_release=self.agregar_usuario)
            ],
            size_hint=(0.9, None),
            height=600
        )
        self.dialogo_agregar.open()

    def mostrar_estado_dropdown(self, instance, touch):
        if instance.collide_point(*touch.pos):
            self.menu_estado.open()

    def seleccionar_estado(self, estado):
        self.estado_field.text = estado
        self.menu_estado.dismiss()

    def mostrar_grupo_dropdown(self, instance, touch):
        if instance.collide_point(*touch.pos):
            self.menu_grupo.open()

    def seleccionar_grupo(self, grupo):
        self.grupo_field.text = grupo
        self.menu_grupo.dismiss()

    def agregar_usuario(self, instance):
        try:
            nuevo = {
                "nombre": self.nombre_field.text.strip(),
                "edad": int(self.edad_field.text.strip()),
                "peso": int(self.peso_field.text.strip()),
                "altura": int(self.altura_field.text.strip()),
                "estado": self.estado_field.text.strip().capitalize(),
                "correo": self.correo_field.text.strip(),
                "enfermedades": self.enfermedades_field.text.strip(),
                "medicamentos": self.medicamentos_field.text.strip(),
                "contacto_emergencia": self.contacto_field.text.strip(),
                "grupo_sanguineo": self.grupo_field.text.strip(),
                "alergias": self.alergias_field.text.strip(),
                "ritmo_cardiaco": [80, 78, 77]  # Simulación inicial
            }
            self.usuarios.append(nuevo)
            self.dialogo_agregar.dismiss()
            self._actualizar_pantalla()
        except Exception as e:
            print("Error al agregar usuario:", e)

    def logout(self, instance):
        self.manager.current = "login"
class TestAdminApp(MDApp):
    def build(self):
        usuarios = [
            {
                "nombre": "Sofi Developer", "estado": "Activo", "edad": 26,
                "peso": 55, "altura": 160, "correo": "sofi@dev.com",
                "enfermedades": "Cansancio de tanto programar",
                "medicamentos": "Un café fuerte",
                "contacto_emergencia": "ChatGPT - 3001234567",
                "grupo_sanguineo": "A+",
                "alergias": "Errores de sintaxis",
                "ritmo_cardiaco": [85, 88, 84]
            }
        ]
        sm = MDScreenManager()
        sm.add_widget(AdminScreen(name="admin", usuarios=usuarios))
        return sm

if __name__ == "__main__":
    TestAdminApp().run()