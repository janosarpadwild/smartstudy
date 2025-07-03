import re, requests
from new_password import NewPassword
from PyQt6.QtWidgets import QWidget
from PyQt6.QtCore import pyqtSignal
from login_ui.forgot_password_form import Ui_forgot_password_form
from utils import utils

class ForgotPassword(QWidget):
    forgot_password_finished = pyqtSignal()
    def __init__(self, session):
        super().__init__()
        # Loading view settings and user settings to self.static and self.user_settings
        utils.load_static(self)
        utils.load_user_settings(self)
        self.session=session
        # Setup view
        self.ui = Ui_forgot_password_form(self.static['login']['font-sizes'])
        self.ui.setupUi(self)
        # Event handlers
        self.ui.new_password_btn.clicked.connect(self.new_password)
        self.ui.validation_btn.clicked.connect(self.validation)
        self.ui.back_to_login_cmd_link_btn.clicked.connect(self.back_to_login)

        # Show the forgot_password window
        self.show()

    #Request new password
    def new_password(self):
        email = self.ui.email_line_edit.text()
        # Validate email format
        if email == '':
            utils.popup_window('Warning', 'Hiányzó mező')
            return
        if not re.match(r'\b[\w.]+@[\w.]+\.\w{2,}\b', email):
            utils.popup_window('Warning', 'Helytelen email cím')
            return
        email = email.strip()
        url = f'{self.user_settings['SERVER_URL']}/new_credentials_request/'
        json = {'action':'new_password','email': email}
        try:
            if url.startswith('https://127.0.0.1'):
                # Localhost SSL verification
                print('get')
                response = self.session.get(url, json=json)                
            else:
                response = self.session.get(url, json=json, verify=True)
            print('after get')
            response_data = response.json()
            message = response_data.get('message')
            error = response_data.get('error')
            if message != None:
                utils.popup_window('Information', message)
            if error != None:
                utils.popup_window('Error', error)
        except (requests.exceptions.RequestException, requests.exceptions.SSLError) as e:
            utils.popup_window('Error', f'Kérés elutasítva a szervertől: {self.user_settings['SERVER_URL']}/new_credentials_request/')

    # Go to the new password creation and verification (new_password)
    def validation(self):
        self.hide()
        self.new_password = NewPassword(self.session)
        self.new_password.new_password_finished.connect(self.back_to_login)
        self.new_password.show()

    # Emit signal to show login window
    def back_to_login(self):
        self.forgot_password_finished.emit()
        self.close()