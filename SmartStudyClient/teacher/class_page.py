import requests
from utils import utils
from PyQt6.QtWidgets import QWidget
from PyQt6.QtCore import pyqtSignal, QRect
from PyQt6.QtGui import QGuiApplication
from teacher.teacher_ui.class_page_form import Ui_class_page
from teacher.student_result_page import StudentResultsPage
from teacher.topic_req_page import TopicRequirementPage

class ClassPage(QWidget):
    class_page_finished = pyqtSignal(QRect)
    def __init__(self, token, class_name, class_id, geometry, session):
        super().__init__()
        # Loading view settings and user settings to self.static and self.user_settings
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

        self.ui = Ui_class_page(self.static['user'][self.user_settings['font-size']])        
        self.ui.setupUi(self)
        # Event handlers
        self.get_courses()
        self.setGeometry(geometry)
        self.resize_window()
        self.ui.font_size_combo_box.currentIndexChanged.connect(self.resize_window)
        self.ui.back_to_main_page_cmd_link_btn.clicked.connect(self.back_to_teacher_main_page)
        self.ui.courses_combo_box.currentIndexChanged.connect(self.ui.topics)
        self.ui.topic_combo_box.currentIndexChanged.connect(lambda: self.ui.topics_result(self))
        self.ui.topic_course_enable_btn.clicked.connect(self.enable_topics)

        #Show class window
        if self.user_settings['maximized']:
            self.showMaximized()
        else:
            self.show()

    # Emit signal to show teacher main window
    def back_to_teacher_main_page(self):
        self.user_settings['maximized'] = self.isMaximized()
        utils.save_settings(self)
        self.class_page_finished.emit(self.geometry())
        self.close()

    # Receive signal to show class window
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
        self.get_courses()
        self.setGeometry(geometry)
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

    # Ger courses for class
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
                self.back_to_teacher_main_page()
                return
            data = response_data.get('courses')
            self.ui.data = data
            self.ui.courses()
            self.ui.refresh(self)
        except (requests.exceptions.RequestException, requests.exceptions.SSLError) as e:
            utils.popup_window('Error', f'Kérés elutasítva a szervertől: {self.user_settings['SERVER_URL']}/smartstudy/')
            self.back_to_teacher_main_page()
            return

    #Go to topic_requirement_page
    def enable_topics(self):        
        if self.ui.courses_combo_box.currentIndex()<1:
            return
        course_id = self.ui.data[self.ui.courses_combo_box.currentIndex()-1]["id"]
        course_name = self.ui.courses_combo_box.currentText()   
        self.user_settings['maximized'] = self.isMaximized()
        utils.save_settings(self)     
        self.topic_req_page = TopicRequirementPage(self.token, self.class_name, self.class_id, course_name, course_id, self.geometry(), self.session)
        self.topic_req_page.topic_req_page_finished.connect(self.return_to_class_page)
        self.topic_req_page.show()
        self.hide()

    # Go to student_results_page
    def student_results(self):
        button = self.sender()
        student_id = int(button.objectName().split('_')[-1])
        student_name = button.objectName().split('_')[-2]
        course_id = self.ui.data[self.ui.courses_combo_box.currentIndex()-1]["id"]
        course_name = self.ui.courses_combo_box.currentText()   
        self.user_settings['maximized'] = self.isMaximized()
        utils.save_settings(self)     
        self.student_results_page = StudentResultsPage(self.token, self.class_id, student_name, student_id, course_name, course_id, self.geometry(), self.session)
        self.student_results_page.student_results_page_finished.connect(self.return_to_class_page)
        self.student_results_page.show()
        self.hide()
