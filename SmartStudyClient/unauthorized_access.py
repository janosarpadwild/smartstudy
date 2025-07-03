import requests
from PyQt6.QtWidgets import QWidget
from PyQt6.QtCore import pyqtSignal
from login_ui.unauthorized_access_form import Ui_unauthorized_access_form
from utils import utils

class UnauthorizedAccess(QWidget):
    unauthorized_access_finished = pyqtSignal()
    def __init__(self, session):
        super().__init__()
        #L oading view settings and user settings to self.static and self.user_settings
        utils.load_static(self)
        utils.load_user_settings(self)
        self.session=session
        # Setup view
        self.ui = Ui_unauthorized_access_form(self.static['login']['font-sizes'])
        self.ui.setupUi(self)
        # Event handlers
        self.ui.back_to_login_cmd_link_btn.clicked.connect(self.back_to_login)
        self.ui.report_btn.clicked.connect(self.lock)

        # Show the unauthorized_access window
        self.show()

    # Lock account with provided code
    def lock(self):
        lock_code = self.ui.lock_code_line_edit.text()
        if lock_code == '':
            utils.popup_window('Warning', 'Hiányzó mező')
            return   
        if len(lock_code)<24:
            utils.popup_window('Warning', 'Túl rövid zárolási kód')
            return
        url = f'{self.user_settings['SERVER_URL']}/lock_account/'
        json = {'action':'lock_account', 'lock_code': lock_code}
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
            utils.popup_window('Error', f'Kérés elutasítva a szervertől: {self.user_settings['SERVER_URL']}/lock_account/')
            
    # Emit signal to show login window
    def back_to_login(self):
        self.unauthorized_access_finished.emit()
        self.close()