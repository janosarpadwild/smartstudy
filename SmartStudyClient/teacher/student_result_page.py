import requests
from PyQt6.QtWidgets import QWidget
from PyQt6.QtCore import pyqtSignal, QRect
from PyQt6.QtGui import QGuiApplication
from teacher.teacher_ui.student_results_page_form import Ui_student_results_page
from utils import utils

class StudentResultsPage(QWidget):
    student_results_page_finished = pyqtSignal(QRect)
    def __init__(self, token, class_id, student_name, student_id, course_name, course_id, geometry, session):
        super().__init__()
        utils.load_static(self)
        utils.load_user_settings(self)
        self.session=session
        self.token = token
        self.class_id = class_id
        self.student_name = student_name
        self.student_id = student_id
        self.course_name = course_name
        self.course_id = course_id
        match self.user_settings['font-size']:
            case "small":
                self.window_size_index = 0
            case "medium":
                self.window_size_index = 1
            case "big":
                self.window_size_index = 2

        self.ui = Ui_student_results_page(self.static['user'][self.user_settings['font-size']])        
        # Button click events
        self.ui.setupUi(self)
        self.get_courses()
        self.setGeometry(geometry)
        self.resize_window()
        self.ui.font_size_combo_box.currentIndexChanged.connect(self.resize_window)
        self.ui.back_to_class_cmd_link_btn.clicked.connect(self.back_to_class_page)
        if self.user_settings['maximized']:
            self.showMaximized()
        else:
            self.show()

    def back_to_class_page(self):
        self.user_settings['maximized'] = self.isMaximized()
        utils.save_settings(self)
        self.student_results_page_finished.emit(self.geometry())
        self.close()

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
            case 1:
                if screen_width<self.static['user']['medium']['window-size']['width'] or screen_height<self.static['user']['medium']['window-size']['height']:
                    if not utils.too_small_screen():
                        self.ui.font_size_combo_box.setCurrentIndex(self.window_size_index)
                        return
                self.user_settings['font-size']='medium'
            case 2:
                if screen_width<self.static['user']['big']['window-size']['width'] or screen_height<self.static['user']['big']['window-size']['height']:
                    if not utils.too_small_screen():
                        self.ui.font_size_combo_box.setCurrentIndex(self.window_size_index)
                        return
                self.user_settings['font-size']='big'
        utils.save_settings(self)
        self.ui.static = self.static['user'][self.user_settings['font-size']]
        self.ui.screen_size(self)
        self.ui.topics(self)

    def get_courses(self):
        url = f'{self.user_settings['SERVER_URL']}/smartstudy/'
        headers = {'Authorization': f'Token {self.token}'}
        json = {'action':'get_student_result', 'class_id':self.class_id, "course_id":self.course_id, 'student_id':self.student_id}

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
            data = response_data.get('student_results')
            self.ui.data = data
            self.ui.topics(self)
        except requests.exceptions.RequestException as e:
            utils.popup_window('Error', f'Kérés elutasítva a szervertől: {self.user_settings['SERVER_URL']}/smartstudy/')
            self.back_to_class_page()
            return

