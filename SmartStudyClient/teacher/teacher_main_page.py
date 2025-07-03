from utils import utils
from teacher.teacher_ui.teacher_main_page_form import Ui_teacher_main_page

from teacher.subtopic_page import SubTopicPage
from teacher.class_page import ClassPage

import requests
from PyQt6.QtWidgets import QWidget
from PyQt6.QtGui import QGuiApplication
from PyQt6.QtCore import QRect

class Teacher(QWidget):
    def __init__(self, token, name, session):
        super().__init__()
        # Loading view settings and user settings to self.static and self.user_settings
        utils.load_static(self)
        utils.load_user_settings(self)
        self.session=session
        self.token = token  
        self.name = name
        # Setup view
        self.ui = Ui_teacher_main_page(self.static['user'][self.user_settings['font-size']])
        

        self.ui.setupUi(self)
        self.get_data("classes")
        self.get_data("subjects_topics")
        self.window_size_index = -1
        self.resize_window()
        match self.user_settings['font-size']:
            case "small":
                self.window_size_index = 0
            case "medium":
                self.window_size_index = 1
            case "big":
                self.window_size_index = 2
        #self.ui.subjects()##
        #self.ui.refresh(self)##
        # Event handlers
        self.ui.font_size_combo_box.currentIndexChanged.connect(self.resize_window)
        self.ui.subject_combo_box.currentIndexChanged.connect(lambda: self.ui.subject_list(self))
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
        self.ui.refresh(self)

    # Request class and subject data from server
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
            self.close()
            return
        if type == "classes":
            self.ui.class_data = data
            self.ui.class_list(self)            
        elif type == "subjects_topics":
            self.ui.subject_data = data
            self.ui.subjects()

    # Go to subtopic_page
    def get_subtopics(self):
        button = self.sender()
        topic_name = button.text()
        topic_id = int(button.objectName().split('_')[-1])     
        self.user_settings['maximized'] = self.isMaximized()
        utils.save_settings(self)   
        self.topic_page = SubTopicPage(self.token, topic_name, topic_id, self.geometry(), self.session)
        self.topic_page.subtopic_page_finished.connect(self.return_to_main_page)
        self.topic_page.show()
        self.hide()

    # Go to class_page
    def get_class(self):
        button = self.sender()
        class_name = button.objectName().split('_')[-2]
        class_id = int(button.objectName().split('_')[-1])   
        self.user_settings['maximized'] = self.isMaximized()
        utils.save_settings(self)     
        self.class_page = ClassPage(self.token, class_name, class_id, self.geometry(), self.session)
        self.class_page.class_page_finished.connect(self.return_to_main_page)
        self.class_page.show()
        self.hide()

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
                return
        except (requests.exceptions.RequestException, requests.exceptions.SSLError) as e:
            utils.popup_window('Error', f'Kérés elutasítva a szervertől: {self.user_settings['SERVER_URL']}/smartstudy/')
            return
        self.close()

    # Receive signal to show teacher main window
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
        self.get_data("subjects_topics")
        self.ui.refresh(self)
        self.setGeometry(geometry)
        if self.user_settings['maximized']:
            self.showMaximized()
        else:
            self.show()
