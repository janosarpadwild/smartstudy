import re, requests
from new_email import NewEmail
from PyQt6.QtWidgets import QWidget
from PyQt6.QtCore import pyqtSignal
from login_ui.change_email_form import Ui_change_email_form
from utils import utils

class ChangeEmail(QWidget):
    change_email_finished = pyqtSignal()
    def __init__(self, session):
        super().__init__()
        # Loading view settings and user settings to self.static and self.user_settings
        utils.load_static(self)
        utils.load_user_settings(self)
        self.session=session
        # Setup view
        self.ui = Ui_change_email_form(self.static['login']['font-sizes'])
        self.ui.setupUi(self)
        # Event handlers
        self.ui.back_to_login_cmd_link_btn.clicked.connect(self.back_to_login)
        self.ui.new_email_btn.clicked.connect(self.new_email)
        self.ui.email_validation_btn.clicked.connect(self.validation)

        # Show the change_email window
        self.show()

    # Change email address
    def new_email(self):
        old_email = self.ui.old_email_line_edit.text()
        new_email_1 = self.ui.new_email_line_edit.text()
        new_email_2 = self.ui.new_email_repeat_line_edit.text()
        password = self.ui.password_line_edit.text()

        if old_email == '' or new_email_1 == '' or new_email_2 == '' or password == '':
            utils.popup_window('Warning', 'Hiányzó mezők')
            return
        pattern = r'\b[\w.]+@[\w.]+\.\w{2,}\b'
        if not re.match(pattern, old_email) or not re.match(pattern, new_email_1) or not re.match(pattern, new_email_2):
            utils.popup_window('Warning', 'Helytelen email cím')
            return
        if new_email_1 != new_email_2:
            utils.popup_window('Warning', 'Az email címek nem egyeznek. Kérlek az új email címet írd be mindkét mezőbe helyesen')
            return
        if len(password)<12:
            utils.popup_window('Warning', 'Túl rövid jelszó')
            return
        pattern = r'^(?=.*[a-z])(?=.*[A-Z])(?=.*\d)(?=.*[!@#$%^&*(),.?":{}|<>]).{8,}$'
        # Check if the password matches the pattern
        if not re.match(pattern, password):        
            utils.popup_window('Warning', 'Helytelen jelszó')
            return
        
        url = f'{self.user_settings['SERVER_URL']}/new_credentials_request/'
        json = {'action':'new_email', 'email':old_email,'new_email': new_email_1, 'new_email_repeat': new_email_2, 'password': password}
        try:
            if url.startswith('https://127.0.0.1'):
                # Localhost SSL verification
                response = self.session.get(url, json=json)                
            else:
                response = self.session.get(url, json=json, verify=True)
            response_data = response.json()
            message = response_data.get('message')
            error = response_data.get('error')
            if message != None:
                utils.popup_window('Information', message)
            if error != None:
                utils.popup_window('Error', error)
        except (requests.exceptions.RequestException, requests.exceptions.SSLError) as e:
            utils.popup_window('Error', f'Kérés elutasítva a szervertől: {self.user_settings['SERVER_URL']}/new_credentials_request/')

    # Go to email verification (new_email)
    def validation(self):
        self.hide()
        self.new_email = NewEmail(self.session)
        self.new_email.new_email_finished.connect(self.back_to_login)
        self.new_email.show()
        
    # Emit signal to show login window
    def back_to_login(self):
        self.change_email_finished.emit()
        self.close()