import requests
from PyQt6.QtWidgets import QWidget
from PyQt6.QtCore import pyqtSignal, QRect
from PyQt6.QtGui import QGuiApplication
from student.student_ui.tutorial_page_form import Ui_tutorial_page
from utils import utils

class TutorialPage(QWidget):
    tutorial_page_finished = pyqtSignal(QRect)
    def __init__(self, token, subtopic_name, subtopic_id, topic_id, topic_name, course_id, geometry, session):
        super().__init__()
        # Loading view settings and user settings to self.static and self.user_settings
        utils.load_static(self)
        utils.load_user_settings(self)
        self.session=session
        self.token = token
        self.subtopic_name = subtopic_name
        self.subtopic_id = subtopic_id
        self.topic_id = topic_id
        self.topic_name = topic_name
        self.course_id = course_id
        self.index = 0
        match self.user_settings['font-size']:
            case "small":
                self.window_size_index = 0
            case "medium":
                self.window_size_index = 1
            case "big":
                self.window_size_index = 2
        self.ui = Ui_tutorial_page(self.static['user'][self.user_settings['font-size']])

        self.ui.setupUi(self)

        self.get_tutorial()
        self.setGeometry(geometry)
        self.resize_window()

        self.ui.font_size_combo_box.currentIndexChanged.connect(self.resize_window)
        self.ui.back_to_topics_cmd_link_btn.clicked.connect(self.back_to_subtopic_main_page)
        
        #self.ui.repeat_animation_btn animation?
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
        self.ui.tutorial(self)

    # Emit signal to show subtopic_page
    def back_to_subtopic_main_page(self):
        self.user_settings['maximized'] = self.isMaximized()
        utils.save_settings(self)
        self.tutorial_page_finished.emit(self.geometry())
        self.close()

    # Get tutorial for subtopic
    def get_tutorial(self):
        url = f'{self.user_settings['SERVER_URL']}/smartstudy/'
        headers = {'Authorization': f'Token {self.token}'}
        json = {'action':'get_tutorial','course_id':self.course_id, 'topic_id':self.topic_id, 'subtopic_id':self.subtopic_id}

        try:
            if url.startswith('https://127.0.0.1'):
                # Localhost SSL verification
                response = self.session.get(url, headers=headers, json=json)                
            else:
                response = self.session.get(url, headers=headers, json=json, verify=True)
            response_data = response.json()
            data = response_data.get('tutorial')
            self.ui.data = data
            self.ui.tutorial(self)
        except (requests.exceptions.RequestException, requests.exceptions.SSLError) as e:
            utils.popup_window('Error', f'Kérés elutasítva a szervertől: {self.user_settings['SERVER_URL']}/smartstudy/')
            self.back_to_subtopic_main_page()

    # Next tutorial page
    def next(self):
        if self.index+1<len(self.ui.data['parameters']):
            self.index += 1
            self.ui.tutorial(self)
            
            self.ui.repeat_animation_btn.setHidden(False)
        else:
            url = f'{self.user_settings['SERVER_URL']}/smartstudy/'
            headers = {'Authorization': f'Token {self.token}'}
            json = {'action':'finished_tutorial','course_id':self.course_id, 'topic_id':self.topic_id, 'subtopic_id':self.subtopic_id}

            try:
                if url.startswith('https://127.0.0.1'):
                    # Localhost SSL verification
                    response = self.session.post(url, headers=headers, json=json)                
                else:
                    response = self.session.post(url, headers=headers, json=json, verify=True)
                response_data = response.json()
            except (requests.exceptions.RequestException, requests.exceptions.SSLError) as e:
                utils.popup_window('Error', f'Kérés elutasítva a szervertől: {self.user_settings['SERVER_URL']}/smartstudy/')
            self.back_to_subtopic_main_page()
