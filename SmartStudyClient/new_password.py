import re, requests
from PyQt6.QtWidgets import QWidget, QLineEdit
from PyQt6.QtGui import QPixmap
from PyQt6.QtCore import pyqtSignal
from login_ui.new_password_form import Ui_new_password_form
from utils import utils

class NewPassword(QWidget):
    new_password_finished = pyqtSignal()
    def __init__(self, session):
        super().__init__()
        # Loading view settings and user settings to self.static and self.user_settings
        utils.load_static(self)
        utils.load_user_settings(self)
        self.session=session
        # Setup view
        self.ui = Ui_new_password_form(self.static['login']['font-sizes'])
        self.ui.setupUi(self)
        # Event handlers
        self.ui.new_password_btn.clicked.connect(self.new_password)
        self.ui.back_to_login_cmd_link_btn.clicked.connect(self.back_to_login)
        self.ui.show_password_check_box.toggled.connect(self.on_checkbox_changed)
        self.ui.new_password_line_edit.textChanged.connect(self.check_password_line_edit)
        self.ui.new_password_repeat_line_edit.textChanged.connect(self.check_password_line_edit)

        # Show the new_password window
        self.show()    

    # Reveal/hide password
    def on_checkbox_changed(self, checked):
        if checked:
            self.ui.new_password_line_edit.setEchoMode(QLineEdit.EchoMode.Normal)
            self.ui.new_password_repeat_line_edit.setEchoMode(QLineEdit.EchoMode.Normal)
        else:
            self.ui.new_password_line_edit.setEchoMode(QLineEdit.EchoMode.Password)
            self.ui.new_password_repeat_line_edit.setEchoMode(QLineEdit.EchoMode.Password)

    def check_password_line_edit(self):
        password = self.ui.new_password_line_edit.text()

        # Check if password has at least one lowercase letter
        if bool(re.search(r'[a-z]', password)):
            self.ui.lower_case_letter_icon_label.setPixmap(QPixmap("utils/images/ok-icon.png"))
        else:
            self.ui.lower_case_letter_icon_label.setPixmap(QPixmap("utils/images/not-ok-icon.png"))

        # Check if password has at least one uppercase letter
        if bool(re.search(r'[A-Z]', password)):
            self.ui.upper_case_letter_icon_label.setPixmap(QPixmap("utils/images/ok-icon.png"))
        else:
            self.ui.upper_case_letter_icon_label.setPixmap(QPixmap("utils/images/not-ok-icon.png"))

        # Check if password has at least one digit
        if bool(re.search(r'\d', password)):
            self.ui.digit_icon_label.setPixmap(QPixmap("utils/images/ok-icon.png"))
        else:
            self.ui.digit_icon_label.setPixmap(QPixmap("utils/images/not-ok-icon.png"))

        # Check if password has at least one special character
        if bool(re.search(r"[\u0021-\u002F\u003A-\u0040\u005B-\u0060\u007B-\u007E]", password)):
            self.ui.special_character_icon_label.setPixmap(QPixmap("utils/images/ok-icon.png"))
        else:
            self.ui.special_character_icon_label.setPixmap(QPixmap("utils/images/not-ok-icon.png"))

        # Check if passowrd at least 12 long
        if len(password)>=12:
            self.ui.password_length_icon_label.setPixmap(QPixmap("utils/images/ok-icon.png"))
        else:
            self.ui.password_length_icon_label.setPixmap(QPixmap("utils/images/not-ok-icon.png"))

        # Check if password and repeated password match
        password_repeat = self.ui.new_password_repeat_line_edit.text()
        if password == password_repeat:
            self.ui.password_repeat_icon_label.setPixmap(QPixmap("utils/images/ok-icon.png"))
        else:
            self.ui.password_repeat_icon_label.setPixmap(QPixmap("utils/images/not-ok-icon.png"))

    # Create new password with provided permission code
    def new_password(self):
        permission_code = self.ui.permission_code_line_edit.text()
        new_password_1 = self.ui.new_password_line_edit.text()
        new_password_2 = self.ui.new_password_repeat_line_edit.text()

        if permission_code == '' or new_password_1 == '' or new_password_2 == '':
            utils.popup_window('Warning', 'Hiányzó mezők')
            return        
        if new_password_1 != new_password_2:
            utils.popup_window('Warning', 'A jelszavak nem egyeznek. Kérlek az új jelszót írd be mindkét mezőbe helyesen')
            return                
        if len(new_password_1)<12:
            utils.popup_window('Warning', 'Túl rövid jelszó')
            return
        if len(permission_code)<24:
            utils.popup_window('Warning', 'Túl rövid megerősítő kód')
            return
        
        pattern = r'^(?=.*[a-z])(?=.*[A-Z])(?=.*\d)(?=.*[!@#$%^&*(),.?":{}|<>]).{8,}$'
        # Check if the password matches the pattern
        if not re.match(pattern, new_password_1):        
            utils.popup_window('Warning', 'Gyenge jelszó')
            return
        
        url = f'{self.user_settings['SERVER_URL']}/change_credentials/'
        json = {'action':'new_password', 'permission_code': permission_code, 'password': new_password_1, 'password_repeat': new_password_2}
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
            utils.popup_window('Error', f'Kérés elutasítva a szervertől: {self.user_settings['SERVER_URL']}/new_credentials_request/')

    # Emit signal to show login window
    def back_to_login(self):
        self.new_password_finished.emit()
        self.close()