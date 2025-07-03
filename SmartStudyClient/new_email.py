import requests
from PyQt6.QtWidgets import QWidget
from PyQt6.QtCore import pyqtSignal
from login_ui.new_email_form import Ui_new_email_form
from utils import utils

class NewEmail(QWidget):
    new_email_finished = pyqtSignal()
    def __init__(self, session):
        super().__init__()
        # Loading view settings and user settings to self.static and self.user_settings
        utils.load_static(self)
        utils.load_user_settings(self)
        self.session=session
        # Setup view
        self.ui = Ui_new_email_form(self.static['login']['font-sizes'])
        # Button click events
        self.ui.setupUi(self)
        self.ui.back_to_login_cmd_link_btn.clicked.connect(self.back_to_login)
        self.ui.new_email_btn.clicked.connect(self.new_email)

        # Show the new_email window
        self.show()

    # Verify the change of email address
    def new_email(self):
        permission_code = self.ui.permission_code_line_edit.text()
        if permission_code == '':
            utils.popup_window('Warning', 'Hiányzó mező')
            return   
        if len(permission_code)<24:
            utils.popup_window('Warning', 'Túl rövid megerősítő kód')
            return
        url = f'{self.user_settings['SERVER_URL']}/change_credentials/'
        json = {'action':'new_email', 'permission_code': permission_code}
        try:
            if url.startswith('https://127.0.0.1'):
                # Localhost SSL verification
                response = self.session.post(url, json=json)                
            else:
                response = self.session.post(url, json=json, verify=True)
            response_data = response.json()
            message = response_data.get('message')
            error = response_data.get('error')
            if message != None:
                utils.popup_window('Information', message)
            if error != None:
                utils.popup_window('Error', error)
        except (requests.exceptions.RequestException, requests.exceptions.SSLError) as e:
            utils.popup_window('Error', f'Kérés elutasítva a szervertől: {self.user_settings['SERVER_URL']}/change_credentials/')
            
    # Emit signal to show login window
    def back_to_login(self):
        self.new_email_finished.emit()
        self.close()