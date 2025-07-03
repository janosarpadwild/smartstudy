import re
from PyQt6.QtWidgets import QWidget
from PyQt6.QtCore import pyqtSignal
from login_ui.new_server_form import Ui_new_server_form
from utils import utils

class NewServer(QWidget):
    new_server_finished = pyqtSignal()
    def __init__(self, session):
        super().__init__()
        # Loading view settings and user settings to self.static and self.user_settings
        utils.load_static(self)
        utils.load_user_settings(self)
        self.session=session
        # Setup view
        self.ui = Ui_new_server_form(self.static['login']['font-sizes'])
        self.ui.setupUi(self)
        # Event handlers
        self.ui.back_to_login_cmd_link_btn.clicked.connect(self.back_to_login)
        self.ui.new_server_btn.clicked.connect(self.new_server)

        # show the login window
        self.show()

    # Save new server address to user_settings
    def new_server(self):
        server_url = self.ui.server_address_line_edit.text()
        if server_url == '':
            utils.popup_window('Warning', 'Hiányzó mező')
            return
        if not re.match(r'\b(?:www\.)?[\w-]+\.\w{2,}(?:\.\w{2,})?/api\b', server_url) and not re.match(r'\b(?:\d{1,3}\.){3}\d{1,3}(:\d{1,5})?/api\b', server_url) and not re.match('localhost:8000/api', server_url): 
            utils.popup_window('Warning', 'Rossz szerver cím')
            return
        self.user_settings['SERVER_URL'] = 'https://'+server_url
        utils.save_settings(self)
        utils.popup_window('Information', 'A szerver új címe elmentésre került')

    # Emit signal to show login window
    def back_to_login(self):
        self.new_server_finished.emit()
        self.close()