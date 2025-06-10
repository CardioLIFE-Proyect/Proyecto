from kivymd.app import MDApp
from kivymd.uix.screenmanager import MDScreenManager

from login_screen import LoginScreen
from registro_screen import RegistroScreen
from recuperar_screen import RecuperarScreen
from admin_screen import AdminScreen
from reportes_screen import ReportesScreen  # Si esta ya está lista

class CardioLifeApp(MDApp):
    def build(self):
        self.title = "CardioLIFE"
        sm = MDScreenManager()

        # Lista de pantallas
        sm.add_widget(LoginScreen(name="login"))
        sm.add_widget(RegistroScreen(name="registro"))
        sm.add_widget(RecuperarScreen(name="recuperar"))
        sm.add_widget(AdminScreen(name="admin"))
        sm.add_widget(ReportesScreen(name="reportes"))  # Si aún no está lista, comenta esta línea

        return sm

if __name__ == "__main__":
    CardioLifeApp().run()
