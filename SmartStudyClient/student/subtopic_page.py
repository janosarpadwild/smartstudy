import requests
from PyQt6.QtWidgets import QWidget
from PyQt6.QtCore import pyqtSignal, QRect
from PyQt6.QtGui import QGuiApplication
from student.student_ui.subtopic_page_form import Ui_subtopic_page
from utils import utils
from student.task_page import TaskPage
from student.tutorial_page import TutorialPage

class SubTopicPage(QWidget):
    subtopic_page_finished = pyqtSignal(QRect)
    def __init__(self, token, course_id, topic_name, topic_id, geometry, session):
        super().__init__()
        # Loading view settings and user settings to self.static and self.user_settings
        utils.load_static(self)
        utils.load_user_settings(self)
        self.session=session
        self.token = token
        self.course_id = course_id
        self.topic_name = topic_name
        self.topic_id = topic_id
        match self.user_settings['font-size']:
            case "small":
                self.window_size_index = 0
            case "medium":
                self.window_size_index = 1
            case "big":
                self.window_size_index = 2

        self.ui = Ui_subtopic_page(self.static['user'][self.user_settings['font-size']])
        self.ui.setupUi(self)
        self.get_subtopics()
        self.get_test_result()
        self.setGeometry(geometry) 
        self.resize_window()
        # Event handlers
        self.ui.font_size_combo_box.currentIndexChanged.connect(self.resize_window)
        self.ui.back_to_main_page_cmd_link_btn.clicked.connect(self.back_to_student_main_page)
        self.ui.test_btn.clicked.connect(self.get_test)

        # Show subtopic window
        if self.user_settings['maximized']:
            self.showMaximized()
        else:
            self.show()

    # Emit signal to show student main page
    def back_to_student_main_page(self):
        self.user_settings['maximized'] = self.isMaximized()
        utils.save_settings(self)
        self.subtopic_page_finished.emit(self.geometry())
        self.close()

    # Receive signal to show subtopic page
    def return_to_subtopic_page(self, geometry:QRect):
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
        self.get_subtopics()
        self.get_test_result()
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
        self.ui.subtopics(self)

    # Get subtopics for course and topic 
    def get_subtopics(self):
        url = f'{self.user_settings['SERVER_URL']}/smartstudy/'
        headers = {'Authorization': f'Token {self.token}'}
        json = {'action':'get_subtopics', 'course_id':self.course_id, 'topic_id':self.topic_id}

        try:
            if url.startswith('https://127.0.0.1'):
                # Localhost SSL verification
                response = self.session.get(url, headers=headers, json=json)                
            else:
                response = self.session.get(url, headers=headers, json=json, verify=True)
            response_data = response.json()
            data = response_data.get('subtopics')
            self.ui.data = data
            self.ui.subtopics(self)
        except (requests.exceptions.RequestException, requests.exceptions.SSLError) as e:
            utils.popup_window('Error', f'Kérés elutasítva a szervertől: {self.user_settings['SERVER_URL']}/smartstudy/')

    # Get tutorial for subtopic
    def get_tutorial(self):
        button = self.sender()
        subtopic_name = button.text()
        subtopic_id = button.objectName().split('_')[-1]

        self.hide()
        self.user_settings['maximized'] = self.isMaximized()
        utils.save_settings(self)
        self.tutorial_page = TutorialPage(self.token, subtopic_name, subtopic_id, self.topic_id, self.topic_name, self.course_id, self.geometry(), self.session)
        self.tutorial_page.tutorial_page_finished.connect(self.return_to_subtopic_page)

    # Get task for subtopic
    def get_practise_task(self):
        button = self.sender()
        subtopic_name = button.text()
        subtopic_id = button.objectName().split('_')[-1]
        self.user_settings['maximized'] = self.isMaximized()
        utils.save_settings(self)
        self.task_page = TaskPage(self.token, subtopic_name, subtopic_id, False, self.topic_id, self.topic_name, self.course_id, self.geometry(), self.session)
        self.task_page.task_page_finished.connect(self.return_to_subtopic_page)
        self.task_page.show()
        self.hide()
    
    # Get test for topic
    def get_test(self):   
        self.user_settings['maximized'] = self.isMaximized()
        utils.save_settings(self)     
        self.task_page = TaskPage(self.token, "", "", True, self.topic_id, self.topic_name, self.course_id, self.geometry(), self.session)
        self.task_page.task_page_finished.connect(self.return_to_subtopic_page)
        self.task_page.show()
        self.hide()

    # Get test results for topic
    def get_test_result(self):
        url = f'{self.user_settings['SERVER_URL']}/smartstudy/'
        headers = {'Authorization': f'Token {self.token}'}
        json = {'action':'get_test_result', 'course_id':self.course_id, 'topic_id':self.topic_id}

        try:
            if url.startswith('https://127.0.0.1'):
                # Localhost SSL verification
                response = self.session.get(url, headers=headers, json=json)                
            else:
                response = self.session.get(url, headers=headers, json=json, verify=True)
            response_data = response.json()
            self.test_result = response_data.get('test_result')
            self.ui.test(self.test_result)
        except (requests.exceptions.RequestException, requests.exceptions.SSLError) as e:
            utils.popup_window('Error', f'Kérés elutasítva a szervertől: {self.user_settings['SERVER_URL']}/smartstudy/')