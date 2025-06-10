from kivymd.uix.screen import MDScreen
from kivymd.uix.boxlayout import MDBoxLayout
from kivymd.uix.button import MDRaisedButton, MDFlatButton
from kivymd.uix.label import MDLabel
from kivymd.uix.card import MDCard
from kivymd.uix.scrollview import MDScrollView
from kivymd.uix.menu import MDDropdownMenu
from kivymd.uix.textfield import MDTextField
from kivymd.uix.selectioncontrol import MDCheckbox
from kivy.metrics import dp
from kivy.graphics import Color, Rectangle
from kivy.uix.image import Image
from kivy.uix.anchorlayout import AnchorLayout
from kivy.uix.floatlayout import FloatLayout
from datetime import datetime
import csv
from kivymd.uix.snackbar import Snackbar
from kivymd.app import MDApp
from kivymd.uix.screenmanager import MDScreenManager



class ReportesScreen(MDScreen):
    def __init__(self, **kwargs):
        usuarios = kwargs.pop("usuarios", [])  # 💥 EXTRAER ANTES de super()
        super().__init__(**kwargs)
        self.usuarios = usuarios  # ✅ ahora sí lo puedes usar

        self.main_layout = MDBoxLayout(orientation='vertical')
        self._crear_toolbar()

        self.scroll = MDScrollView()
        self.content = MDBoxLayout(orientation='vertical', spacing=20, padding=30, size_hint_y=None)
        self.content.bind(minimum_height=self.content.setter("height"))

        self._crear_filtros()
        self._crear_opciones_reporte()
        self._crear_botones_accion()

        self.scroll.add_widget(self.content)
        self.main_layout.add_widget(self.scroll)
        self.add_widget(self.main_layout)

    def _crear_toolbar(self):
        toolbar = MDBoxLayout(orientation='horizontal', size_hint_y=None, height=70, padding=[10, 0, 10, 0])
        with toolbar.canvas.before:
            self.gradient_rects_2 = []
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
                self.gradient_rects_2.append(rect)

        def update_gradient(instance, value):
            if hasattr(self, 'gradient_rects_2'):
                toolbar_width = instance.size[0]
                strip_width = toolbar_width / len(self.gradient_rects_2)
                for i, rect in enumerate(self.gradient_rects_2):
                    rect.pos = (instance.pos[0] + i * strip_width, instance.pos[1])
                    rect.size = (strip_width, instance.size[1])
        toolbar.bind(pos=update_gradient, size=update_gradient)

        title_label = MDLabel(text="Reportes\nSistema", font_style="Caption", theme_text_color="Custom", text_color=(1, 1, 1, 1), halign="left", valign="middle", size_hint_x=0.33)
        logo_center = AnchorLayout(anchor_x='center', anchor_y='center', size_hint_x=0.34)
        logo = Image(source="assets/logb.png", size_hint=(None, None), size=(100, 100), allow_stretch=True, keep_ratio=True)
        logo_center.add_widget(logo)

        right_box = FloatLayout(size_hint_x=0.33)
        back_btn = MDRaisedButton(text="Volver", on_release=self.volver, size_hint=(None,None), size=(100,40), pos_hint={"right":1, "center_y": 0.5})
        right_box.add_widget(back_btn)

        toolbar.add_widget(title_label)
        toolbar.add_widget(logo_center)
        toolbar.add_widget(right_box)

        self.main_layout.add_widget(toolbar)

    def _crear_filtros(self):
        card = MDCard(orientation='vertical', padding=13, size_hint_y=None, adaptive_height=True, elevation=2, radius=[8])
        title = MDLabel(text="Filtros de Reporte", font_style="H6", size_hint_y=None, height=90)

        estado_box = MDBoxLayout(orientation='horizontal', size_hint_y=None, height=60, spacing=15)
        estado_label = MDLabel(text="Estado de usuario:", size_hint_x=0.8)

        self.estado_dropdown = MDTextField(text="Todos", readonly=True, size_hint_x=0.9, icon_right="menu-down", mode="rectangle")
        self.estado_dropdown.bind(on_touch_down=self._mostrar_menu_estado_click)

        estado_box.add_widget(estado_label)
        estado_box.add_widget(self.estado_dropdown)

        edad_box = MDBoxLayout(orientation='horizontal', size_hint_y=None, height=80, spacing=10)
        edad_label = MDLabel(text="Rango de edad:", size_hint_x=0.5)
        edad_inputs = MDBoxLayout(orientation='horizontal', size_hint_x=0.5, spacing=25)
        self.edad_min = MDTextField(hint_text="Mín", input_filter="int", size_hint_x=0.5)
        self.edad_max = MDTextField(hint_text="Máx", input_filter="int", size_hint_x=0.5)
        edad_inputs.add_widget(self.edad_min)
        edad_inputs.add_widget(self.edad_max)
        edad_box.add_widget(edad_label)
        edad_box.add_widget(edad_inputs)

        card.add_widget(title)
        card.add_widget(estado_box)
        card.add_widget(edad_box)

        self.content.add_widget(card)

    def _mostrar_menu_estado_click(self, instance, touch):
        if instance.collide_point(*touch.pos):
            estados = ["Todos", "Activo", "Inactivo"]
            items = [{"text": estado, "viewclass": "OneLineListItem", "on_release": lambda x=estado: self._seleccionar_estado(x)} for estado in estados]
            self.menu = MDDropdownMenu(caller=instance, items=items, width_mult=2.0)
            self.menu.open()
        return True

    def _seleccionar_estado(self, estado):
        self.estado_dropdown.text = estado
        self.menu.dismiss()

    def _crear_opciones_reporte(self):
        card = MDCard(orientation='vertical', padding=10, size_hint_y=None, adaptive_height=True, elevation=2, radius=[8])
        title = MDLabel(text="Tipo de Reporte", font_style="H6", size_hint_y=None, height=60)

        opciones_box = MDBoxLayout(orientation='vertical', spacing=10, adaptive_height=True)

        self.check_general = self._crear_check_item("Reporte General", True)
        self.check_salud = self._crear_check_item("Estadísticas de Salud", False)
        self.check_alertas = self._crear_check_item("Alertas y Anomalías", False)
        self.check_actividad = self._crear_check_item("Nivel de Actividad", False)

        opciones_box.add_widget(self.check_general)
        opciones_box.add_widget(self.check_salud)
        opciones_box.add_widget(self.check_alertas)
        opciones_box.add_widget(self.check_actividad)

        formato_box = MDBoxLayout(orientation='horizontal', size_hint_y=None, height=110, padding=[20, 10, 20, 10], spacing=10)

        formato_label = MDLabel(text="Formato de salida:", size_hint_y=None, height=90, halign="left", valign="middle")

        dropdown_container = MDBoxLayout(size_hint=(1, None), height=90)

        self.formato_dropdown = MDRaisedButton(text="PDF", size_hint=(1, None), height=50, pos_hint={"center_y": 0.5})
        self.formato_dropdown.bind(on_release=self._mostrar_menu_formato)

        dropdown_container.add_widget(self.formato_dropdown)

        formato_box.add_widget(formato_label)
        formato_box.add_widget(dropdown_container)

        card.add_widget(title)
        card.add_widget(opciones_box)
        card.add_widget(formato_box)

        self.content.add_widget(card)

    def _crear_check_item(self, texto, valor_predeterminado=False):
        item = MDBoxLayout(orientation='horizontal', size_hint_y=None, height=40)
        checkbox = MDCheckbox(active=valor_predeterminado, size_hint=(None, None), size=(48, 48))
        label = MDLabel(text=texto)
        item.add_widget(checkbox)
        item.add_widget(label)
        return item

    def _mostrar_menu_formato(self, instance):
        formatos = ["PDF", "Excel", "CSV", "Texto plano"]
        items = [{"text": formato, "viewclass": "OneLineListItem", "on_release": lambda x=formato: self._seleccionar_formato(x)} for formato in formatos]
        self.menu_formato = MDDropdownMenu(caller=instance, items=items, width_mult=3)
        self.menu_formato.open()

    def _seleccionar_formato(self, formato):
        self.formato_dropdown.text = formato
        self.menu_formato.dismiss()

    def _crear_botones_accion(self):
        box = MDBoxLayout(orientation='horizontal', size_hint_y=None, height=60, spacing=8)

        generar_btn = MDRaisedButton(text="Generar Reporte", size_hint=(1, None), height=50, md_bg_color=(89/255, 38/255, 209/255), on_release=self.generar_reporte)
        cancelar_btn = MDRaisedButton(text="Cancelar", size_hint=(1, None), height=50, md_bg_color=(0.7, 0.7, 0.7, 1), on_release=self.volver)

        box.add_widget(generar_btn)
        box.add_widget(cancelar_btn)
        self.content.add_widget(box)

    def generar_reporte(self, instance):
        # Actualizar lista de usuarios si fuera necesario
        estado_filtro = self.estado_dropdown.text
        try:
            edad_min = int(self.edad_min.text) if self.edad_min.text else 0
            edad_max = int(self.edad_max.text) if self.edad_max.text else 120
        except ValueError:
            edad_min, edad_max = 0, 120

        formato = self.formato_dropdown.text

        usuarios_filtrados = self.usuarios
        if estado_filtro != "Todos":
            usuarios_filtrados = [u for u in usuarios_filtrados if u["estado"] == estado_filtro]

        usuarios_filtrados = [u for u in usuarios_filtrados if edad_min <= u["edad"] <= edad_max]

        self._mostrar_vista_previa(usuarios_filtrados, formato)

    def _mostrar_vista_previa(self, usuarios_filtrados, formato):
        self.usuarios_filtrados = usuarios_filtrados
        self.content.clear_widgets()

        title = MDLabel(text=f"Vista Previa de Reporte ({formato})", font_style="H6", size_hint_y=None, height=50)
        self.content.add_widget(title)

        resumen = MDCard(orientation='vertical', padding=20, spacing=10, size_hint_y=None, adaptive_height=True, elevation=2, radius=[10])

        resumen.add_widget(MDLabel(text=f"Total de usuarios filtrados: {len(usuarios_filtrados)}", theme_text_color="Primary", halign="left", size_hint_y=None, height=30))

        if usuarios_filtrados:
            edad_prom = sum(u["edad"] for u in usuarios_filtrados) / len(usuarios_filtrados)
            peso_prom = sum(u["peso"] for u in usuarios_filtrados) / len(usuarios_filtrados)
            altura_prom = sum(u["altura"] for u in usuarios_filtrados) / len(usuarios_filtrados)

            resumen.add_widget(MDLabel(text=f"Edad promedio: {round(edad_prom)} años", halign="left", size_hint_y=None, height=30))
            resumen.add_widget(MDLabel(text=f"Peso promedio: {round(peso_prom)} kg", halign="left", size_hint_y=None, height=30))
            resumen.add_widget(MDLabel(text=f"Altura promedio: {round(altura_prom)} cm", halign="left", size_hint_y=None, height=30))

        self.content.add_widget(resumen)

        if usuarios_filtrados:
            lista_title = MDLabel(text="Usuarios en el Reporte:", font_style="H6", size_hint_y=None, height=40)
            self.content.add_widget(lista_title)

            for u in usuarios_filtrados:
                card = MDCard(orientation='vertical', padding=15, spacing=8, size_hint_y=None, adaptive_height=True, elevation=1, radius=[6])

                layout = MDBoxLayout(orientation="vertical", spacing=6, adaptive_height=True)

                prom_ritmo = round(sum(u["ritmo_cardiaco"]) / len(u["ritmo_cardiaco"]), 1)
                estado_color = (0.2, 0.7, 0.3, 1) if u["estado"] == "Activo" else (0.9, 0.3, 0.3, 1)

                layout.add_widget(MDLabel(text=f"[b]Nombre:[/b] {u['nombre']}", markup=True, size_hint_y=None, height=25))
                layout.add_widget(MDLabel(text=f"[b]Edad:[/b] {u['edad']} años", markup=True, size_hint_y=None, height=25))
                layout.add_widget(MDLabel(text=f"[b]Estado:[/b] {u['estado']}", markup=True, size_hint_y=None, height=25, theme_text_color="Custom", text_color=estado_color))
                layout.add_widget(MDLabel(text=f"[b]Correo:[/b] {u['correo']}", markup=True, size_hint_y=None, height=25))
                layout.add_widget(MDLabel(text=f"[b]Promedio ritmo cardíaco:[/b] {prom_ritmo} bpm", markup=True, size_hint_y=None, height=25))

                card.add_widget(layout)
                self.content.add_widget(card)
        else:
            self.content.add_widget(MDLabel(text="No se encontraron usuarios que cumplan con los filtros.", theme_text_color="Secondary"))

        box = MDBoxLayout(orientation='horizontal', size_hint_y=None, height=60, spacing=8, padding=[0, 20, 0, 0])

        download_btn = MDRaisedButton(text=f"Descargar {formato}", size_hint=(1, None), height=50, md_bg_color=(0.2, 0.7, 0.3, 1), on_release=lambda x: self._simular_descarga(formato))
        volver_btn = MDRaisedButton(text="Volver a Filtros", size_hint=(1, None), height=50, md_bg_color=(0.6, 0.4, 0.8, 1), on_release=lambda x: self._reiniciar_pantalla())

        box.add_widget(download_btn)
        box.add_widget(volver_btn)
        self.content.add_widget(box)

    def _simular_descarga(self, formato):
        try:
            if not hasattr(self, 'usuarios_filtrados') or not self.usuarios_filtrados:
                Snackbar(text="No hay usuarios filtrados para exportar").open()
                return

            usuarios = self.usuarios_filtrados
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            nombre_archivo = f"reporte_{formato.lower()}_{timestamp}"

            if formato == "Texto plano":
                ruta = f"{nombre_archivo}.txt"
                with open(ruta, "w", encoding="utf-8") as archivo:
                    archivo.write("========================================\n")
                    archivo.write("        INFORME MÉDICO DE USUARIOS\n")
                    archivo.write("========================================\n\n")
                    for idx, u in enumerate(usuarios, start=1):
                        prom_ritmo = round(sum(u["ritmo_cardiaco"]) / len(u["ritmo_cardiaco"]))
                        archivo.write(f"Paciente #{idx}\n")
                        archivo.write("----------------------------------------\n")
                        archivo.write(f"Nombre completo       : {u['nombre']}\n")
                        archivo.write(f"Edad                  : {u['edad']} años\n")
                        archivo.write(f"Peso                  : {u['peso']} kg\n")
                        archivo.write(f"Altura                : {u['altura']} cm\n")
                        archivo.write(f"Correo electrónico    : {u['correo']}\n")
                        archivo.write(f"Estado del paciente   : {u['estado']}\n")
                        archivo.write(f"Grupo sanguíneo       : {u['grupo_sanguineo']}\n")
                        archivo.write(f"Alergias              : {u['alergias']}\n")
                        archivo.write(f"Enfermedades previas  : {u['enfermedades']}\n")
                        archivo.write(f"Medicamentos actuales : {u['medicamentos']}\n")
                        archivo.write(f"Contacto de emergencia: {u['contacto_emergencia']}\n")
                        archivo.write(f"Ritmo cardíaco promedio: {prom_ritmo} bpm\n")
                        archivo.write(f"Historial ritmo cardíaco: {u['ritmo_cardiaco']}\n")
                        archivo.write("\n")
                    archivo.write("===== FIN DEL INFORME =====\n")

            elif formato == "CSV":
                ruta = f"{nombre_archivo}.csv"
                with open(ruta, "w", newline="", encoding="utf-8") as archivo:
                    writer = csv.writer(archivo)
                    writer.writerow(["Nombre", "Edad", "Estado", "Correo", "Promedio Ritmo", "Ritmo Histórico"])
                    for u in usuarios:
                        prom_ritmo = round(sum(u["ritmo_cardiaco"]) / len(u["ritmo_cardiaco"]))
                        writer.writerow([
                            u["nombre"],
                            u["edad"],
                            u["estado"],
                            u["correo"],
                            prom_ritmo,
                            str(u["ritmo_cardiaco"])
                        ])

            else:
                Snackbar(text=f"Formato '{formato}' no soportado aún.").open()
                return

            Snackbar(text=f"✅ Informe guardado como: {ruta}").open()

            from kivy.clock import Clock
            Clock.schedule_once(lambda dt: setattr(self.manager, 'current', 'admin'), 2)

        except Exception as e:
            print("❌ Error al exportar:", e)
            Snackbar(text="❌ Error al generar el informe").open()

    def _reiniciar_pantalla(self):
        self.content.clear_widgets()
        self._crear_filtros()
        self._crear_opciones_reporte()
        self._crear_botones_accion()

    def volver(self, instance=None):
        self.manager.current = "admin"
class CardioApp(MDApp):
    def build(self):
        usuarios = [
            {
                "nombre": "Sofi González", "estado": "Activo", "edad": 26,
                "peso": 60, "altura": 165, "correo": "sofi@example.com",
                "enfermedades": "Hipertensión", "medicamentos": "Losartán",
                "contacto_emergencia": "Mamá - 3001234567", "grupo_sanguineo": "A+",
                "alergias": "Ninguna", "ritmo_cardiaco": [82, 78, 76]
            },
            {
                "nombre": "Julián Torres", "estado": "Inactivo", "edad": 31,
                "peso": 75, "altura": 172, "correo": "julian@example.com",
                "enfermedades": "Arritmia", "medicamentos": "Atenolol",
                "contacto_emergencia": "Papá - 3109876543", "grupo_sanguineo": "O-",
                "alergias": "Penicilina", "ritmo_cardiaco": [110, 105, 108]
            }
        ]

        sm = MDScreenManager()
        sm.add_widget(ReportesScreen(name="reportes", usuarios=usuarios))
        return sm

if __name__ == "__main__":
    CardioApp().run()
