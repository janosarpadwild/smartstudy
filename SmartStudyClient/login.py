import re, sys, requests
import requests.sessions
from utils import utils

from secretary.secretary_main_page import Secretary
from student.student_main_page import Student
from teacher.teacher_main_page import Teacher

from forgot_password import ForgotPassword
from change_email import ChangeEmail
from new_server import NewServer
from unauthorized_access import UnauthorizedAccess

from PyQt6.QtWidgets import QApplication, QWidget, QLineEdit
from login_ui.login_form import Ui_login_form

from requests.adapters import HTTPAdapter, Retry
#from urllib3.util.retry import Retry

class Login(QWidget):
    def __init__(self):
        super().__init__()
        # Loading view settings and user settings to self.static and self.user_settings
        utils.load_static(self)
        utils.load_user_settings(self)

        retry = Retry(
            total=5,
            backoff_factor=0.1,
            status_forcelist=[500, 502, 503, 504]
        )

        adapter = HTTPAdapter(max_retries=retry, pool_connections=10, pool_maxsize=10)
        self.session = requests.Session()
        self.session.mount("https://", adapter)
        self.session.verify = 'certificate/localhost.crt'

        # Setup view
        self.ui = Ui_login_form(self.static['login']['font-sizes'])
        self.ui.setupUi(self)
        # Event handlers
        self.ui.login_btn.clicked.connect(self.login)
        self.ui.forgot_password_cmd_link_btn.clicked.connect(self.forgot_password)
        self.ui.change_email_cmd_link_btn.clicked.connect(self.change_email)
        self.ui.new_server_cmd_link_btn.clicked.connect(self.new_server)
        self.ui.unathorized_cmd_link_btn.clicked.connect(self.unauthorized_access)
        self.ui.show_password_check_box.toggled.connect(self.on_checkbox_changed)

        # Show the login window
        self.show()    

    def login(self):
        """self.close()
        self.student = Secretary('token', 'asdasd')
        self.student.show()
        return"""
        email = self.ui.email_line_edit.text()
        password = self.ui.password_line_edit.text()

        if email == '' or password == '':
            utils.popup_window('Warning', 'Hiányzó mezők')
            return
        # Validate email format
        if not re.match(r'\b[\w.]+@[\w.]+\.\w{2,}\b', email):
            utils.popup_window('Warning', 'Helytelen email cím')
            return        
        if len(password)<12:
            utils.popup_window('Warning', 'Túl rövid jelszó')
            return
        url = f'{self.user_settings['SERVER_URL']}/login/'
        json = {'action':'login','email': email, 'password': password}
        try:
            if url.startswith('https://127.0.0.1'):
                # Localhost SSL verification
                response = self.session.post(url, json=json)
            else:
                response = self.session.post(url, json=json, verify=True)
            response_data = response.json()
            user_category = response_data.get('user_category')
            error = response_data.get('error')
            if error != None:
                utils.popup_window('Error', error)
                return
        except (requests.exceptions.RequestException, requests.exceptions.SSLError) as e:
            utils.popup_window('Error', f'Kérés elutasítva a szervertől: {self.user_settings['SERVER_URL']}/login/')
            return        
        # Redirect to user page
        match user_category:
            case 'STUDENT':
                self.student = Student(response_data.get('token'), response_data.get('name'), self.session)
                self.student.show()
            case 'TEACHER':
                self.teacher = Teacher(response_data.get('token'), response_data.get('name'), self.session)
                self.teacher.show()
            case 'SECRETARY':
                self.secretary = Secretary(response_data.get('token'), response_data.get('name'), self.session)
                self.secretary.show()
        self.close()
        
    # Reveal/hide password
    def on_checkbox_changed(self, checked):
        if checked:
            self.ui.password_line_edit.setEchoMode(QLineEdit.EchoMode.Normal)
        else:
            self.ui.password_line_edit.setEchoMode(QLineEdit.EchoMode.Password)

    # Go to password reset (forgot_password)
    def forgot_password(self):        
        self.forgot_password = ForgotPassword(self.session)
        self.forgot_password.forgot_password_finished.connect(self.return_to_login)
        self.forgot_password.show()
        self.hide()
    
    # Go to email change (change_email)
    def change_email(self):        
        self.change_email = ChangeEmail(self.session)
        self.change_email.change_email_finished.connect(self.return_to_login)
        self.change_email.show()
        self.hide()
    
    # Go to new server address set up (new_server)
    def new_server(self):        
        self.new_server = NewServer(self.session)
        self.new_server.new_server_finished.connect(self.return_to_login)
        self.new_server.show()
        self.hide()

    # Go to account lock (unauthorized_access)
    def unauthorized_access(self):        
        self.unauthorized_access = UnauthorizedAccess(self.session)
        self.unauthorized_access.unauthorized_access_finished.connect(self.return_to_login)
        self.unauthorized_access.show()
        self.hide()

    # Receive signal to show login window
    def return_to_login(self):
        self.show()

if __name__ == '__main__':
    app = QApplication(sys.argv)
    login_window = Login()
    sys.exit(app.exec())
