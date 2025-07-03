import requests
from PyQt6.QtWidgets import QWidget
from PyQt6.QtCore import pyqtSignal, QRect, QSize
from PyQt6.QtGui import QGuiApplication
from secretary.secretary_ui.course_page_form import Ui_course_page, DeleteDialog
from utils import utils

class CoursePage(QWidget):
    course_page_finished = pyqtSignal(QRect)
    def __init__(self, token, class_name, class_id, geometry, session):
        super().__init__()
        utils.load_static(self)
        utils.load_user_settings(self)
        self.session=session
        self.token = token
        self.class_name = class_name
        self.class_id = class_id
        match self.user_settings['font-size']:
            case "small":
                self.window_size_index = 0
            case "medium":
                self.window_size_index = 1
            case "big":
                self.window_size_index = 2
   

        self.ui = Ui_course_page(self.static['user'][self.user_settings['font-size']])
        self.ui.setupUi(self)

        self.get_data("subjects")
        self.get_data("teachers_subjects")
        self.get_courses()
        self.setGeometry(geometry)
        self.resize_window()
        self.ui.font_size_combo_box.currentIndexChanged.connect(self.resize_window)
        self.ui.back_to_main_page_cmd_link_btn.clicked.connect(self.back_to_class_page)
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
        self.ui.course_list(self)

    def remove_teacher(self):
        remove_btn = self.sender()
        teacher_id = int(remove_btn.objectName().split('_')[-1])
        course_id = int(remove_btn.objectName().split('_')[-2])
        url = f'{self.user_settings['SERVER_URL']}/smartstudy/'
        headers = {'Authorization': f'Token {self.token}'}
        json = {'action':'remove_teacher', 'course_id':course_id, 'teacher_id':teacher_id}
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
        self.get_courses()
        self.ui.course_list(self)

    def add_teacher_enable(self):
        teacher_combo_box = self.sender()
        index1 = int(teacher_combo_box.objectName().split('_')[-1])
        add_teacher_button = self.ui.course_list_grid_layout.itemAtPosition(index1, 2).widget()
        if teacher_combo_box.currentText()=="":
            add_teacher_button.setEnabled(False)
        else:
            add_teacher_button.setEnabled(True)
    
    def add_teacher(self):
        add_teacher_button = self.sender()
        index1 = int(add_teacher_button.objectName().split('_')[-1])
        teacher_combo_box = self.ui.course_list_grid_layout.itemAtPosition(index1, 1).widget()
        teacher_id = int(teacher_combo_box.currentData())
        course_id = int(add_teacher_button.objectName().split('_')[-2])
        url = f'{self.user_settings['SERVER_URL']}/smartstudy/'
        headers = {'Authorization': f'Token {self.token}'}
        json = {'action':'add_teacher', 'class_id':self.class_id, 'course_id':course_id, 'teacher_id':teacher_id}
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
        self.get_courses()
        self.ui.course_list(self)
    
    def save_enable(self):
        course_name_line_edit = self.sender()
        index = int(course_name_line_edit.objectName().split('_')[-1])
        save_button = self.ui.course_list_grid_layout.itemAtPosition(index, 2).widget()
        #course_names = [i['course_name'] for i in self.ui.course_data]
        if course_name_line_edit.text()=="" or course_name_line_edit.text().endswith(" "):
            save_button.setEnabled(False)
        else:
            save_button.setEnabled(True)

    def save_course(self):
        button = self.sender()
        id = int(button.objectName().split('_')[-1])
        index = int(button.objectName().split('_')[-2])
        course_name = self.ui.course_list_grid_layout.itemAtPosition(index, 0).widget().text()
        url = f'{self.user_settings['SERVER_URL']}/smartstudy/'
        headers = {'Authorization': f'Token {self.token}'}
        json = {'action':'save_course', 'course_id':id, 'course_name':course_name}
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
        self.get_courses()
        self.ui.course_list(self)

    def delete_course(self):
        dialog = DeleteDialog(self.ui.static["font-sizes"]["text"], QSize(self.ui.static["topic"]["small-width"]-40, self.ui.static["topic"]["height"]))
        accept = dialog.accept_delete()
        if not accept:
            return
        button = self.sender()
        id = int(button.objectName().split('_')[-1])
        url = f'{self.user_settings['SERVER_URL']}/smartstudy/'
        headers = {'Authorization': f'Token {self.token}'}
        json = {'action':'delete_course', 'course_id':id}
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
        self.get_courses()
        self.ui.course_list(self)

    def subject_enable(self):
        course_name_line_edit = self.sender()
        index = int(course_name_line_edit.objectName().split('_')[-1])
        subject_combo_box = self.ui.course_list_grid_layout.itemAtPosition(index, 1).widget()
        if course_name_line_edit.text()=="" and not course_name_line_edit.text().endswith(" "):
            subject_combo_box.setCurrentIndex(0)
            subject_combo_box.setEnabled(False)
        else:
            subject_combo_box.setEnabled(True)

    def add_course_enable(self):
        subject_combo_box = self.sender()
        index = int(subject_combo_box.objectName().split('_')[-1])
        save_button = self.ui.course_list_grid_layout.itemAtPosition(index, 2).widget()
        if subject_combo_box.currentText()=="":
            save_button.setEnabled(False)
        else:
            save_button.setEnabled(True)

    def new_course(self):
        button = self.sender()
        index = int(button.objectName().split('_')[-1])
        course_name = self.ui.course_list_grid_layout.itemAtPosition(index, 0).widget().text()
        subject_name = self.ui.course_list_grid_layout.itemAtPosition(index, 1).widget().currentText()
        course_names = [i['course_name'] for i in self.ui.course_data]        
        if course_name in course_names:
            utils.popup_window('Information', f'Nem lehet egy osztálynak két ugyanolyan nevű kurzusa ({course_name})')
            return
        url = f'{self.user_settings['SERVER_URL']}/smartstudy/'
        headers = {'Authorization': f'Token {self.token}'}
        json = {'action':'new_course', 'class_id':self.class_id, 'course_name':course_name, 'subject_name':subject_name}
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
        self.get_courses()
        self.ui.course_list(self)

    def get_data(self, type):
        url = f'{self.user_settings['SERVER_URL']}/smartstudy/'
        headers = {'Authorization': f'Token {self.token}'}
        json = {'action':f'get_{type}'}
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
                self.back_to_class_page()
                return
            data = response_data.get(type)
        except (requests.exceptions.RequestException, requests.exceptions.SSLError) as e:
            utils.popup_window('Error', f'Kérés elutasítva a szervertől: {self.user_settings['SERVER_URL']}/smartstudy/')
            self.back_to_class_page()
            return
        match type:
            case "teachers_subjects":
                self.ui.teacher_data = data
            case "subjects":
                self.ui.subject_data = data

    def get_courses(self):
        url = f'{self.user_settings['SERVER_URL']}/smartstudy/'
        headers = {'Authorization': f'Token {self.token}'}
        json = {'action':'get_courses', 'class_id':self.class_id}
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
                self.back_to_class_page()
                return
            data = response_data.get("courses")
            self.ui.course_data = data
            self.ui.course_list(self)
        except (requests.exceptions.RequestException, requests.exceptions.SSLError) as e:
            utils.popup_window('Error', f'Kérés elutasítva a szervertől: {self.user_settings['SERVER_URL']}/smartstudy/')
            self.back_to_class_page()
            return
        
    def back_to_class_page(self):
        self.user_settings['maximized'] = self.isMaximized()
        utils.save_settings(self)
        self.course_page_finished.emit(self.geometry())
        self.close()