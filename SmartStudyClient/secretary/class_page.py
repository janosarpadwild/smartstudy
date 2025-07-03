import requests
from PyQt6.QtWidgets import QWidget, QFormLayout
from PyQt6.QtCore import pyqtSignal, QRect, QSize
from PyQt6.QtGui import QGuiApplication, QIcon
from secretary.secretary_ui.class_page_form import Ui_class_page, ClassDialog, StudentDialog, DeleteDialog
from secretary.course_page import CoursePage
from utils import utils

class ClassPage(QWidget):
    class_page_finished = pyqtSignal(QRect)
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
        self.student_select_list = []
        self.ui = Ui_class_page(self.static['user'][self.user_settings['font-size']])   

        self.ui.setupUi(self)
        if class_id !=-1:
            self.get_students()
        self.get_classes()
        print(self.ui.class_data)
        
        self.setGeometry(geometry)
        self.resize_window()

        self.ui.font_size_combo_box.currentIndexChanged.connect(self.resize_window)
        self.ui.courses_btn.clicked.connect(self.course_edit)
        self.ui.back_to_main_page_cmd_link_btn.clicked.connect(self.back_to_secretary_main_page)
        self.ui.save_btn.clicked.connect(self.save)
        self.ui.new_student_btn.clicked.connect(self.student_edit)
        self.ui.student_action_combo_box.currentIndexChanged.connect(self.student_action_choice)
        self.ui.student_action_btn.clicked.connect(self.student_action)
        self.ui.edit_transmission_btn.clicked.connect(self.transmit_class)
        self.ui.delete_class_btn.clicked.connect(self.delete_class)
        self.ui.class_name_line_edit.textChanged.connect(self.class_name_changed)
        if self.user_settings['maximized']:
            self.showMaximized()
        else:
            self.show()

    def return_to_class_page(self, geometry:QRect):
        utils.load_user_settings(self)
        match self.user_settings['font-size']:
            case "small":
                self.window_size_index = 0
                self.ui.font_size_combo_box.setCurrentIndex(0)
            case "medium":
                self.window_size_index = 1
                self.ui.font_size_combo_box.setCurrentIndex(1)
            case "big":
                self.window_size_index = 2
                self.ui.font_size_combo_box.setCurrentIndex(2)
        self.ui.static = self.static['user'][self.user_settings['font-size']]
        self.get_students()
        self.setGeometry(geometry)   
        self.ui.refresh(self)     
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
        self.ui.refresh(self)

    def save(self):
        self.class_name = self.ui.class_name_line_edit.text().strip()
        url = f'{self.user_settings['SERVER_URL']}/smartstudy/'
        headers = {'Authorization': f'Token {self.token}'}
        json = {'action':'new_class', 'name':self.class_name, 'class_id':self.class_id}
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
            self.class_id = response_data.get('class_id')
        except (requests.exceptions.RequestException, requests.exceptions.SSLError) as e:
            utils.popup_window('Error', f'Kérés elutasítva a szervertől: {self.user_settings['SERVER_URL']}/smartstudy/')
            return
        self.ui.courses_btn.setEnabled(True)
        self.ui.student_action_combo_box.setEnabled(True)
        self.ui.new_student_btn.setEnabled(True)
        self.ui.edit_transmission_btn.setEnabled(True)
        self.ui.delete_class_btn.setEnabled(True)

    def class_name_changed(self):
        if self.ui.class_name_line_edit.text()=="":
            self.ui.courses_btn.setEnabled(False)
            self.ui.student_action_combo_box.setEnabled(False)
            self.ui.student_action_combo_box.setCurrentIndex(0)
            self.ui.new_student_btn.setEnabled(False)
            self.ui.edit_transmission_btn.setEnabled(False)
            self.ui.delete_class_btn.setEnabled(False)
            self.ui.save_btn.setEnabled(False)
        else:
            self.ui.save_btn.setEnabled(True)

    def get_students(self):
        url = f'{self.user_settings['SERVER_URL']}/smartstudy/'
        headers = {'Authorization': f'Token {self.token}'}
        json = {'action':'get_students_by_class', 'class_id':self.class_id}
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
            data = response_data.get("students")
            self.ui.student_data = data
            self.ui.student_list(self)            
        except (requests.exceptions.RequestException, requests.exceptions.SSLError) as e:
            utils.popup_window('Error', f'Kérés elutasítva a szervertől: {self.user_settings['SERVER_URL']}/smartstudy/')
            self.back_to_secretary_main_page()
            return
        self.student_select_list = [[False,student['id']] for student in self.ui.student_data]
        self.ui.refresh(self)

    def get_classes(self):
        url = f'{self.user_settings['SERVER_URL']}/smartstudy/'
        headers = {'Authorization': f'Token {self.token}'}
        json = {'action':'get_classes', 'class_id':self.class_id}
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
                return
            data = response_data.get("classes")
            self.ui.class_data = data
            self.ui.student_list(self)
        except (requests.exceptions.RequestException, requests.exceptions.SSLError) as e:
            utils.popup_window('Error', f'Kérés elutasítva a szervertől: {self.user_settings['SERVER_URL']}/smartstudy/')
            return

    def course_edit(self):
        self.user_settings['maximized'] = self.isMaximized()
        utils.save_settings(self)
        self.course_page = CoursePage(self.token, self.class_name, self.class_id, self.geometry(), self.session)
        self.course_page.course_page_finished.connect(self.return_to_class_page)
        self.course_page.show()
        self.hide()

    def student_edit(self):
        button = self.sender()
        student_name = button.objectName().split('_')[-2]
        student_id = int(button.objectName().split('_')[-1])
        if student_id == -1:
            self.student_register("", -1, "")
        else:
            student_id = int(button.objectName().split('_')[-1])
            email = self.get_email_by_id(student_id, self.ui.student_data)
            self.student_register(student_name, student_id, email)

    def student_register(self, student_name, student_id, email):
        dialog = StudentDialog(self.ui.static["font-sizes"]["text"], QSize(self.ui.static["topic"]["small-width"]-40, self.ui.static["topic"]["height"]), student_name, email)
        student_name, email, new = dialog.get_selected_id()
        if student_name=="" or email=="":
            return
        url = f'{self.user_settings['SERVER_URL']}/smartstudy/'
        headers = {'Authorization': f'Token {self.token}'}
        if new or student_id==-1:
            json = {'action':'new_student', "email":email.strip(), "name":student_name.strip(), "class_id":self.class_id}
        else:            
            json = {'action':'edit_student', "id":student_id, "name":student_name.strip()}
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
            self.get_students()
        except (requests.exceptions.RequestException, requests.exceptions.SSLError) as e:
            utils.popup_window('Error', f'Kérés elutasítva a szervertől: {self.user_settings['SERVER_URL']}/smartstudy/')
            return
        if new:
            self.student_register("", -1, "")

    def get_email_by_id(self, id, user_list):
        for user in user_list:
            if user["id"] == id:
                return user["email"]
        return ""

    def back_to_secretary_main_page(self):
        self.user_settings['maximized'] = self.isMaximized()
        utils.save_settings(self)
        self.class_page_finished.emit(self.geometry())
        self.close()

    def student_action_choice(self):
        selected = [student[0] for student in self.student_select_list]
        if self.ui.student_action_combo_box.currentText()!="" and any(selected):
            self.ui.student_action_btn.setEnabled(True)
        else:
            self.ui.student_action_btn.setEnabled(False)

    def student_select(self):
        button = self.sender()
        index = int(button.objectName().split('_')[-2])
        self.student_select_list[index-1][0]=not self.student_select_list[index-1][0]
        if self.student_select_list[index-1][0]:
            button.setIcon(QIcon("utils/images/ok-icon.png"))            
        else:
            button.setIcon(QIcon("utils/images/not-ok-icon.png"))
        self.student_action_choice()
            
    def student_select_all(self):
        button = self.sender()
        selected = [student[0] for student in self.student_select_list]
        if all(selected):
            button.setIcon(QIcon("utils/images/not-ok-icon.png"))
            for i in range(self.ui.student_select_form_layout.rowCount()):
                button = self.ui.student_select_form_layout.itemAt(i, QFormLayout.ItemRole.LabelRole).widget()
                button.setIcon(QIcon("utils/images/not-ok-icon.png"))
            self.student_select_list = [[False,student['id']] for student in self.ui.student_data]
        else:
            button.setIcon(QIcon("utils/images/ok-icon.png"))
            for i in range(self.ui.student_select_form_layout.rowCount()):
                button = self.ui.student_select_form_layout.itemAt(i, QFormLayout.ItemRole.LabelRole).widget()
                button.setIcon(QIcon("utils/images/ok-icon.png"))
            self.student_select_list = [[True,student['id']] for student in self.ui.student_data]
        self.student_action_choice()

    def student_action(self):
        students = [student[1] for student in self.student_select_list if student[0]]
        match self.ui.student_action_combo_box.currentText():
            case "Hozzáadás osztályhoz":
                action = "add_to_class"
                dialog = ClassDialog(self.ui.class_data, self.ui.static["font-sizes"]["text"], QSize(self.ui.static["topic"]["small-width"]-40, self.ui.static["topic"]["height"]))
                class_id = dialog.get_selected_id()
                if class_id == -1:
                    return
            case "Archiválás":
                action = "archive"
            case "Leadás kezelésből":
                action = "discharge"
        url = f'{self.user_settings['SERVER_URL']}/smartstudy/'
        headers = {'Authorization': f'Token {self.token}'}
        if self.ui.student_action_combo_box.currentText()=="Hozzáadás osztályhoz":            
            json = {'action':action, 'students':students, 'class_id':class_id}
        else:
            json = {'action':action, "user":"student", 'user_ids':students}
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
        self.get_students()

    def transmit_class(self):
        url = f'{self.user_settings['SERVER_URL']}/smartstudy/'
        headers = {'Authorization': f'Token {self.token}'}
        json = {'action':'transmit_class', 'id':self.class_id}
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
        self.back_to_secretary_main_page()

    def delete_class(self):
        dialog = DeleteDialog(self.ui.static["font-sizes"]["text"], QSize(self.ui.static["topic"]["small-width"]-40, self.ui.static["topic"]["height"]))
        accept = dialog.accept_delete()
        if not accept:
            return
        url = f'{self.user_settings['SERVER_URL']}/smartstudy/'
        headers = {'Authorization': f'Token {self.token}'}
        json = {'action':'delete_class', 'id':self.class_id}
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
        self.back_to_secretary_main_page()
