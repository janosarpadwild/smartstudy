from utils import utils
from secretary.secretary_ui.secretary_main_page_form import Ui_secretary_main_page, ClassDialog, StudentDialog
from secretary.class_page import ClassPage
from secretary.teacher_page import TeacherPage
import requests
from PyQt6.QtWidgets import QWidget, QFormLayout
from PyQt6.QtGui import QGuiApplication, QIcon
from PyQt6.QtCore import QRect, QSize

class Secretary(QWidget):
    def __init__(self, token, name, session):
        super().__init__()
        utils.load_static(self)
        utils.load_user_settings(self)
        self.session=session
        self.token = token
        self.name = name
        self.ui = Ui_secretary_main_page(self.static['user'][self.user_settings['font-size']])

        self.ui.setupUi(self)
        self.get_data("classes")
        self.get_data("teachers")
        self.get_data("students")
        self.window_size_index = -1
        self.resize_window()
        match self.user_settings['font-size']:
            case "small":
                self.window_size_index = 0
            case "medium":
                self.window_size_index = 1
            case "big":
                self.window_size_index = 2
        self.ui.font_size_combo_box.currentIndexChanged.connect(self.resize_window)
        self.ui.class_combo_box.currentIndexChanged.connect(self.class_order)
        self.ui.new_class_btn.clicked.connect(self.class_edit)

        self.ui.new_teacher_btn.clicked.connect(self.teacher_edit)
        self.ui.teacher_combo_box.currentIndexChanged.connect(self.teacher_order)
        self.ui.teacher_action_combo_box.currentIndexChanged.connect(self.teacher_action_choice)
        self.ui.teacher_action_btn.clicked.connect(self.teacher_action)

        self.ui.new_student_btn.clicked.connect(self.student_edit)
        self.ui.student_combo_box.currentIndexChanged.connect(self.student_order)
        self.ui.student_action_combo_box.currentIndexChanged.connect(self.student_action_choice)
        self.ui.student_action_btn.clicked.connect(self.student_action)

        self.ui.logout_cmd_link_btn.clicked.connect(self.logout)
        if self.user_settings['maximized']:
            self.showMaximized()
        else:
            self.show()

    def return_to_main_page(self, geometry:QRect):
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
        self.get_data("classes")        
        self.get_data("teachers")        
        self.get_data("students")
        self.class_order()
        self.teacher_order()
        self.teacher_order()
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
                self.close()
                return
            data = response_data.get(type)
        except (requests.exceptions.RequestException, requests.exceptions.SSLError) as e:
            utils.popup_window('Error', f'Kérés elutasítva a szervertől: {self.user_settings['SERVER_URL']}/smartstudy/')
            return
        match type:
            case "classes":
                self.ui.class_data = data
                #self.ui.class_list(self)
            case "teachers":
                self.ui.teacher_data = data
                #self.ui.teacher_list(self)
            case "students":
                self.ui.student_data = data
                #self.ui.student_list(self)

    def class_edit(self):
        button = self.sender()
        class_name = button.objectName().split('_')[-2]
        class_id = int(button.objectName().split('_')[-1])
        if class_id==-1:
            self.user_settings['maximized'] = self.isMaximized()
            utils.save_settings(self)
            self.class_page = ClassPage(self.token, "", -1, self.geometry(), self.session)
        else:
            if button.text()=="Szerkesztés":
                self.user_settings['maximized'] = self.isMaximized()
                utils.save_settings(self)
                self.class_page = ClassPage(self.token, class_name, class_id, self.geometry(), self.session)
            else:
                url = f'{self.user_settings['SERVER_URL']}/smartstudy/'
                headers = {'Authorization': f'Token {self.token}'}
                json = {'action':"take_class", "id":class_id}
                try:
                    if url.startswith('https://127.0.0.1'):
                        # Localhost SSL verification
                        response = self.session.post(url, headers=headers, json=json)
                    else:
                        response = self.session.post(url, headers=headers, json=json, verify=True)
                        """response = self.session.post(url, headers=headers, json=json)                
                    else:
                        response = self.session.post(url, headers=headers, json=json, verify=True)"""
                    response_data = response.json()
                    error = response_data.get('error')
                    if error != None:
                        utils.popup_window('Error', error)
                        return
                        #self.close()
                except (requests.exceptions.RequestException, requests.exceptions.SSLError) as e:
                    utils.popup_window('Error', f'Kérés elutasítva a szervertől: {self.user_settings['SERVER_URL']}/smartstudy/')
                    return
                self.get_data("classes")
                self.class_order()
                return
        self.class_page.class_page_finished.connect(self.return_to_main_page)
        self.class_page.show()
        self.hide()

    def teacher_edit(self):
        button = self.sender()
        teacher_name = button.objectName().split('_')[-2]
        teacher_id = int(button.objectName().split('_')[-1])
        if teacher_id ==-1:
            self.user_settings['maximized'] = self.isMaximized()
            utils.save_settings(self)
            self.teacher_page = TeacherPage(self.token, "", -1, "", self.geometry(), self.session)
        else:
            email = self.get_email_by_id(teacher_id, self.ui.teacher_data)
            self.user_settings['maximized'] = self.isMaximized()
            utils.save_settings(self)
            self.teacher_page = TeacherPage(self.token, teacher_name, teacher_id, email, self.geometry(), self.session)
        self.teacher_page.teacher_page_finished.connect(self.return_to_main_page)
        self.teacher_page.show()
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
            json = {'action':'new_student', "email":email.strip(), "name":student_name.strip(), "class_id":-1}
        else:            
            json = {'action':'edit_student', "id":student_id, "name":student_name.strip()}
        try:
            if url.startswith('https://127.0.0.1'):
                # Localhost SSL verification
                response = self.session.post(url, headers=headers, json=json)
            else:
                response = self.session.post(url, headers=headers, json=json, verify=True)
                """response = self.session.post(url, headers=headers, json=json)                
            else:
                response = self.session.post(url, headers=headers, json=json, verify=True)"""
            response_data = response.json()
            error = response_data.get('error')
            if error != None:
                utils.popup_window('Error', error)
                return
        except (requests.exceptions.RequestException, requests.exceptions.SSLError) as e:
            utils.popup_window('Error', f'Kérés elutasítva a szervertől: {self.user_settings['SERVER_URL']}/smartstudy/')
            return
        self.get_data("students")
        if new:
            self.student_register("", -1, "")

    def get_email_by_id(self, id, user_list):
        for user in user_list:
            if user["id"] == id:
                return user["email"]
        return ""

    def logout(self):
        url = f'{self.user_settings['SERVER_URL']}/smartstudy/'
        headers = {'Authorization': f'Token {self.token}'}
        json = {'action':'logout'}
        try:
            if url.startswith('https://127.0.0.1'):
                # Localhost SSL verification
                response = self.session.post(url, headers=headers, json=json)
            else:
                response = self.session.post(url, headers=headers, json=json, verify=True)
                """response = self.session.post(url, headers=headers, json=json)                
            else:
                response = self.session.post(url, headers=headers, json=json, verify=True)"""
            response_data = response.json()
            error = response_data.get('error')
            if error != None:
                utils.popup_window('Error', error)
                return
        except (requests.exceptions.RequestException, requests.exceptions.SSLError) as e:
            utils.popup_window('Error', f'Kérés elutasítva a szervertől: {self.user_settings['SERVER_URL']}/smartstudy/')
            return
        self.close()

    def class_order(self):
        order = self.ui.class_combo_box.currentText()
        self.ui.class_list(self, order)
    
    def teacher_order(self):
        self.ui.teacher_list(self, self.ui.teacher_combo_box.currentText())  
        self.teacher_select_list = [[False,teacher['id']] for teacher in self.ui.teacher_lines]
        self.ui.teacher_action_btn.setEnabled(False)

    def teacher_action_choice(self):
        selected = [teacher[0] for teacher in self.teacher_select_list]
        if self.ui.teacher_combo_box.currentText()!="" and self.ui.teacher_action_combo_box.currentText()!="" and any(selected):
            self.ui.teacher_action_btn.setEnabled(True)
        else:
            self.ui.teacher_action_btn.setEnabled(False)
    
    def teacher_select(self):
        button = self.sender()
        index = int(button.objectName().split('_')[-2])
        self.teacher_select_list[index-1][0]=not self.teacher_select_list[index-1][0]
        if self.teacher_select_list[index-1][0]:
            button.setIcon(QIcon("utils/images/ok-icon.png"))
        else:
            button.setIcon(QIcon("utils/images/not-ok-icon.png"))
        self.teacher_action_choice()

    def teacher_select_all(self):
        button = self.sender()
        if self.ui.teacher_combo_box.currentText()=="":
            return
        selected = [teacher[0] for teacher in self.teacher_select_list]
        if all(selected):
            button.setIcon(QIcon("utils/images/not-ok-icon.png"))
            for i in range(self.ui.teacher_select_form_layout.rowCount()):
                button = self.ui.teacher_select_form_layout.itemAt(i, QFormLayout.ItemRole.LabelRole).widget()
                button.setIcon(QIcon("utils/images/not-ok-icon.png"))
            """for row in range(1, len(self.ui.teacher_lines)):
                button = self.ui.new_teacher_grid_layout.itemAtPosition(row, 0).widget()
                button.setIcon(QIcon("utils/images/not-ok-icon.png"))"""            
            self.teacher_select_list = [[False,teacher['id']] for teacher in self.ui.teacher_lines]
        else:
            button.setIcon(QIcon("utils/images/ok-icon.png"))
            for i in range(self.ui.teacher_select_form_layout.rowCount()):
                button = self.ui.teacher_select_form_layout.itemAt(i, QFormLayout.ItemRole.LabelRole).widget()
                button.setIcon(QIcon("utils/images/ok-icon.png"))
            """for row in range(1, len(self.ui.teacher_lines)):
                button = self.ui.new_teacher_grid_layout.itemAtPosition(row, 0).widget()
                button.setIcon(QIcon("utils/images/ok-icon.png"))"""
            self.teacher_select_list = [[True,teacher['id']] for teacher in self.ui.teacher_lines]
        self.teacher_action_choice()
    
    def teacher_action(self):
        teachers = [teacher[1] for teacher in self.teacher_select_list if teacher[0]]
        match self.ui.teacher_action_combo_box.currentText():
            case "Felvétel kezelésbe":
                action = "admission"
            case "Leadás kezelésből":
                action = "discharge"
            case "Archiválás":
                action = "archive"
        url = f'{self.user_settings['SERVER_URL']}/smartstudy/'
        headers = {'Authorization': f'Token {self.token}'}
        json = {'action':action, "user":"teacher", 'user_ids':teachers}
        try:
            if url.startswith('https://127.0.0.1'):
                # Localhost SSL verification
                response = self.session.post(url, headers=headers, json=json)
            else:
                response = self.session.post(url, headers=headers, json=json, verify=True)
                """response = self.session.post(url, headers=headers, json=json)                
            else:
                response = self.session.post(url, headers=headers, json=json, verify=True)"""
            response_data = response.json()
            error = response_data.get('error')
            if error != None:
                utils.popup_window('Error', error)
                return
        except (requests.exceptions.RequestException, requests.exceptions.SSLError) as e:
            utils.popup_window('Error', f'Kérés elutasítva a szervertől: {self.user_settings['SERVER_URL']}/smartstudy/')
            return
        self.get_data("teachers")
        self.teacher_order()
    
    def student_order(self):
        self.ui.student_list(self, self.ui.student_combo_box.currentText())
        self.student_select_list = [[False,student['id']] for student in self.ui.student_lines]
        self.ui.student_action_btn.setEnabled(False)

    def student_action_choice(self):
        selected = [student[0] for student in self.student_select_list]
        if self.ui.student_combo_box.currentText()!="" and self.ui.student_action_combo_box.currentText()!="" and any(selected):
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
        if self.ui.student_combo_box.currentText()=="":
            return
        selected = [student[0] for student in self.student_select_list]
        if all(selected):
            button.setIcon(QIcon("utils/images/not-ok-icon.png"))
            for i in range(self.ui.student_select_form_layout.rowCount()):
                button = self.ui.student_select_form_layout.itemAt(i, QFormLayout.ItemRole.LabelRole).widget()
                button.setIcon(QIcon("utils/images/not-ok-icon.png"))
            """for row in range(1, len(self.ui.student_lines)):
                button = self.ui.new_student_grid_layout.itemAtPosition(row, 0).widget()
                button.setIcon(QIcon("utils/images/not-ok-icon.png"))"""
            self.student_select_list = [[False,student['id']] for student in self.ui.student_lines]
        else:
            button.setIcon(QIcon("utils/images/ok-icon.png"))
            for i in range(self.ui.student_select_form_layout.rowCount()):
                button = self.ui.student_select_form_layout.itemAt(i, QFormLayout.ItemRole.LabelRole).widget()
                button.setIcon(QIcon("utils/images/ok-icon.png"))
            """for row in range(1, len(self.ui.student_lines)):
                button = self.ui.new_student_grid_layout.itemAtPosition(row, 0).widget()
                button.setIcon(QIcon("utils/images/ok-icon.png"))"""
            self.student_select_list = [[True,student['id']] for student in self.ui.student_lines]
        self.student_action_choice()

    def student_action(self):
        students = [student[1] for student in self.student_select_list if student[0]]
        match self.ui.student_action_combo_box.currentText():
            case "Hozzáadás osztályhoz":
                action = "add_to_class"
                class_input = [i for i in self.ui.class_data if i["secretary_name"]==self.name]
                dialog = ClassDialog(class_input, self.ui.static["font-sizes"]["text"], QSize(self.ui.static["topic"]["small-width"]-40, self.ui.static["topic"]["height"]))
                class_id = dialog.get_selected_id()
                if class_id == -1:
                    return
            case "Felvétel kezelésbe":
                action = "admission"
            case "Leadás kezelésből":
                action = "discharge"
            case "Archiválás":
                action = "archive"
        url = f'{self.user_settings['SERVER_URL']}/smartstudy/'
        headers = {'Authorization': f'Token {self.token}'}
        if self.ui.student_action_combo_box.currentText()=="Hozzáadás osztályhoz":            
            json = {'action':action, "user":"student", 'students':students, 'class_id':class_id}
        else:
            json = {'action':action, "user":"student", 'user_ids':students}
        try:
            if url.startswith('https://127.0.0.1'):
                # Localhost SSL verification
                response = self.session.post(url, headers=headers, json=json)
            else:
                response = self.session.post(url, headers=headers, json=json, verify=True)
                """response = self.session.post(url, headers=headers, json=json)                
            else:
                response = self.session.post(url, headers=headers, json=json, verify=True)"""
            response_data = response.json()
            error = response_data.get('error')
            if error != None:
                utils.popup_window('Error', error)
                return
        except (requests.exceptions.RequestException, requests.exceptions.SSLError) as e:
            utils.popup_window('Error', f'Kérés elutasítva a szervertől: {self.user_settings['SERVER_URL']}/smartstudy/')
            return
        self.get_data("students")
        self.student_order()