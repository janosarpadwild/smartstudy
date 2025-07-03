import re
import requests
from PyQt6.QtWidgets import QWidget, QLineEdit
from PyQt6.QtCore import pyqtSignal, QRect
from PyQt6.QtGui import QGuiApplication
from secretary.secretary_ui.teacher_page_form import Ui_teacher_page
from utils import utils

class TeacherPage(QWidget):
    teacher_page_finished = pyqtSignal(QRect)
    def __init__(self, token, teacher_name, teacher_id, email, geometry, session):
        super().__init__()
        utils.load_static(self)
        utils.load_user_settings(self)
        self.session=session
        self.token = token
        self.teacher_name = teacher_name
        self.teacher_id = teacher_id
        self.email = email
        match self.user_settings['font-size']:
            case "small":
                self.window_size_index = 0
            case "medium":
                self.window_size_index = 1
            case "big":
                self.window_size_index = 2
      

        self.ui = Ui_teacher_page(self.static['user'][self.user_settings['font-size']])
        self.ui.setupUi(self)

        if teacher_id!=-1:
            self.get_teacher_subjects()
        self.get_subjects()
        self.setGeometry(geometry)
        self.resize_window()
        self.ui.font_size_combo_box.currentIndexChanged.connect(self.resize_window)
        self.ui.back_to_main_page_cmd_link_btn.clicked.connect(self.back_to_secretary_main_page)
        self.ui.save_btn.clicked.connect(self.save)
        self.ui.save_and_new_btn.clicked.connect(self.save)
        self.ui.subject_combo_box.currentTextChanged.connect(self.enable_subject_add)
        self.ui.teacher_name_line_edit.textChanged.connect(self.save_enabled)
        if type(self.ui.teacher_email_line_edit)==QLineEdit:
            self.ui.teacher_email_line_edit.textChanged.connect(self.save_enabled)
        if self.user_settings['maximized']:
            self.showMaximized()
        else:
            self.show()

    def resize_window(self):        
        selected_index = self.ui.font_size_combo_box.currentIndex()
        # When the user at the end do not want to change the font we need to correct the combo box which triggers the event again
        if selected_index == self.window_size_index:
            return
        screen_geometry = QGuiApplication.primaryScreen().geometry()
        screen_width = screen_geometry.width()
        screen_height = screen_geometry.height()
        match selected_index:
            case 0:
                self.user_settings['font-size']='small'
                self.window_size_index = 0
            case 1:
                if screen_width<self.static['user']['medium']['window-size']['width'] or screen_height<self.static['user']['medium']['window-size']['height']:
                    if not utils.too_small_screen():
                        self.ui.font_size_combo_box.setCurrentIndex(self.window_size_index)
                        return
                self.user_settings['font-size']='medium'
                self.window_size_index = 1
            case 2:
                if screen_width<self.static['user']['big']['window-size']['width'] or screen_height<self.static['user']['big']['window-size']['height']:
                    if not utils.too_small_screen():
                        self.ui.font_size_combo_box.setCurrentIndex(self.window_size_index)
                        return
                self.user_settings['font-size']='big'
                self.window_size_index = 2
        utils.save_settings(self)
        self.ui.static = self.static['user'][self.user_settings['font-size']]
        self.ui.screen_size(self)
        self.ui.subject_list(self)

    def save_enabled(self):
        if self.ui.teacher_name_line_edit.text()=="" or self.ui.teacher_email_line_edit.text()=="" or self.ui.teacher_name_line_edit.text().endswith(" ") or not re.match(r'\b[\w.]+@[\w.]+\.\w{2,}\b', self.ui.teacher_email_line_edit.text()):
            self.ui.save_btn.setEnabled(False)
            self.ui.save_and_new_btn.setEnabled(False)
        else:
            self.ui.save_btn.setEnabled(True)
            self.ui.save_and_new_btn.setEnabled(True)
        
    def save(self):
        button = self.sender()
        action = button.text()
        self.teacher_name = self.ui.teacher_name_line_edit.text()
        self.email = self.ui.teacher_email_line_edit.text()
        if self.teacher_name =="" or self.email=="":
            return
        url = f'{self.user_settings['SERVER_URL']}/smartstudy/'
        headers = {'Authorization': f'Token {self.token}'}
        if self.teacher_id ==-1:
            json = {'action':'new_teacher', 'email':self.email, 'name':self.teacher_name.strip(), 'subjects':self.ui.teacher_subjects}
        else:
            json = {'action':'edit_teacher', 'id':self.teacher_id, 'name':self.teacher_name.strip(), 'subjects':self.ui.teacher_subjects}
        try:
            if url.startswith('https://127.0.0.1'):
                # Localhost SSL verification
                response = self.session.post(url, headers=headers, json=json)                
            else:
                response = self.session.post(url, headers=headers, json=json, verify=True)
            response_data = response.json()
            error = response_data.get('error')
            if error != None:
                utils.popup_window('Error', error)
                return
        except (requests.exceptions.RequestException, requests.exceptions.SSLError) as e:
            utils.popup_window('Error', f'Kérés elutasítva a szervertől: {self.user_settings['SERVER_URL']}/smartstudy/')
            return
        if action == "Mentés":
            self.back_to_secretary_main_page()
        else:
            self.ui.teacher_name_line_edit.setText("")
            self.ui.teacher_email_line_edit.setText("")
            self.teacher_id = -1
            self.teacher_name = ""
            self.email = ""

    def get_teacher_subjects(self):
        url = f'{self.user_settings['SERVER_URL']}/smartstudy/'
        headers = {'Authorization': f'Token {self.token}'}
        json = {'action':'get_teacher_subjects', 'teacher_id':self.teacher_id}
        try:
            if url.startswith('https://127.0.0.1'):
                # Localhost SSL verification
                response = self.session.get(url, headers=headers, json=json)                
            else:
                response = self.session.get(url, headers=headers, json=json, verify=True)
            response_data = response.json()            
            error = response_data.get('error')
            if error != None:
                utils.popup_window('Error', error)
                self.back_to_secretary_main_page()
                return
            self.ui.teacher_subjects = response_data.get("teacher_subjects")
            self.ui.subject_list(self)
        except (requests.exceptions.RequestException, requests.exceptions.SSLError) as e:
            utils.popup_window('Error', f'Kérés elutasítva a szervertől: {self.user_settings['SERVER_URL']}/smartstudy/')
            self.back_to_secretary_main_page()
            return

    def get_subjects(self):
        url = f'{self.user_settings['SERVER_URL']}/smartstudy/'
        headers = {'Authorization': f'Token {self.token}'}
        json = {'action':'get_subjects'}
        try:
            if url.startswith('https://127.0.0.1'):
                # Localhost SSL verification
                response = self.session.get(url, headers=headers, json=json)                
            else:
                response = self.session.get(url, headers=headers, json=json, verify=True)
            response_data = response.json()            
            error = response_data.get('error')
            if error != None:
                utils.popup_window('Error', error)
                self.back_to_secretary_main_page()
                return
            self.ui.subject_data = response_data.get("subjects")
            self.ui.subjects()
        except (requests.exceptions.RequestException, requests.exceptions.SSLError) as e:
            utils.popup_window('Error', f'Kérés elutasítva a szervertől: {self.user_settings['SERVER_URL']}/smartstudy/')
            self.back_to_secretary_main_page()
            return
        
    def enable_subject_add(self):
        if self.ui.subject_combo_box.currentText() == "":
            self.ui.add_subject_btn.setEnabled(False)
        else:
            self.ui.add_subject_btn.setEnabled(True)

    def remove_subject(self):
        button = self.sender()
        subject = button.objectName().split('_')[-1]
        self.ui.teacher_subjects.remove(subject)
        self.ui.subjects()
        self.ui.subject_list(self)
    
    def add_subject(self):
        subject = self.ui.subject_combo_box.currentText()
        if subject!="":
            self.ui.teacher_subjects.append(subject)
        self.ui.subjects()
        self.ui.subject_list(self)

    def back_to_secretary_main_page(self):
        self.user_settings['maximized'] = self.isMaximized()
        utils.save_settings(self)
        self.teacher_page_finished.emit(self.geometry())
        self.close()