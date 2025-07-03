"Authorization:Token token=<API_Token>"
from utils import utils
from student.student_ui.student_main_page_form import Ui_student_main_page
from PyQt6.QtWidgets import QWidget
from PyQt6.QtGui import QGuiApplication
from PyQt6.QtCore import QRect
import requests
from student.subtopic_page import SubTopicPage

class Student(QWidget):
    def __init__(self, token, name, session):
        super().__init__()
        # Loading view settings and user settings to self.static and self.user_settings
        utils.load_static(self)
        utils.load_user_settings(self)
        self.session=session
        self.token = token
        self.name = name
        # Setup view
        self.ui = Ui_student_main_page(self.static['user'][self.user_settings['font-size']])

        self.ui.setupUi(self)
        self.get_topics()
        self.window_size_index = -1
        self.resize_window()
        match self.user_settings['font-size']:
            case "small":
                self.window_size_index = 0
            case "medium":
                self.window_size_index = 1
            case "big":
                self.window_size_index = 2
        #self.ui.topics(self)##
        # Event handlers
        self.ui.font_size_combo_box.currentIndexChanged.connect(self.resize_window)
        self.ui.logout_cmd_link_btn.clicked.connect(self.logout)
        
        # Show main window
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
        self.ui.topics(self)

    # Request the student related topics list from the server
    def get_topics(self):
        url = f'{self.user_settings['SERVER_URL']}/smartstudy/'
        headers = {'Authorization': f'Token {self.token}'}
        json = {'action':'get_topics'}
        try:
            if url.startswith('https://127.0.0.1'):
                # Localhost SSL verification
                response = self.session.get(url, headers=headers, json=json)                
            else:
                response = self.session.get(url, headers=headers, json=json, verify=True)
            response_data = response.json()
            data = response_data.get('topics')
            error = response_data.get('error')
            if error != None:
                utils.popup_window('Error', error)
                self.close()
            self.ui.data = data
            self.ui.topics(self)
        except (requests.exceptions.RequestException, requests.exceptions.SSLError) as e:
            utils.popup_window('Error', f'Kérés elutasítva a szervertől: {self.user_settings['SERVER_URL']}/smartstudy/')
            self.close()   

    # Go to sub_topic_page
    def get_subtopics(self):
        button = self.sender()
        topic_name = button.text()
        topic_id = button.objectName().split('_')[-1]
        course_id = button.objectName().split('_')[-2]  
        self.user_settings['maximized'] = self.isMaximized()
        utils.save_settings(self)      
        self.topic_page = SubTopicPage(self.token, course_id, topic_name, topic_id, self.geometry(), self.session)
        self.topic_page.subtopic_page_finished.connect(self.return_to_main_page)
        self.topic_page.show()
        self.hide()

    # REceive signal to show student main window
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
        self.get_topics()
        self.setGeometry(geometry)
        if self.user_settings['maximized']:
            self.showMaximized()
        else:
            self.show()

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
            response_data = response.json()
            error = response_data.get('error')
            if error != None:
                utils.popup_window('Error', error)
                self.close()
        except (requests.exceptions.RequestException, requests.exceptions.SSLError) as e:
            utils.popup_window('Error', f'Kérés elutasítva a szervertől: {self.user_settings['SERVER_URL']}/smartstudy/')
            self.close()
        self.close()
