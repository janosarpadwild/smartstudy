import requests
from PyQt6.QtWidgets import QWidget, QLineEdit
from PyQt6.QtCore import pyqtSignal, QRect
from PyQt6.QtGui import QGuiApplication, QIcon
from teacher.teacher_ui.topic_req_page_form import Ui_topic_req_page
from utils import utils

class TopicRequirementPage(QWidget):
    topic_req_page_finished = pyqtSignal(QRect)
    def __init__(self, token, class_name, class_id, course_name, course_id, geometry, session):
        super().__init__()
        utils.load_static(self)
        utils.load_user_settings(self)
        self.session=session
        self.token = token
        self.class_id = class_id
        self.class_name = class_name
        self.course_name = course_name
        self.course_id = course_id
        match self.user_settings['font-size']:
            case "small":
                self.window_size_index = 0
            case "medium":
                self.window_size_index = 1
            case "big":
                self.window_size_index = 2

        self.ui = Ui_topic_req_page(self.static['user'][self.user_settings['font-size']])        
        # Button click events
        self.ui.setupUi(self)
        self.get_topics()
        self.setGeometry(geometry)
        self.resize_window()
        self.ui.font_size_combo_box.currentIndexChanged.connect(self.resize_window)
        self.ui.back_to_class_cmd_link_btn.clicked.connect(self.back_to_class_page)
        self.ui.save_btn.clicked.connect(self.save)
        if self.user_settings['maximized']:
            self.showMaximized()
        else:
            self.show()

    def back_to_class_page(self):
        self.user_settings['maximized'] = self.isMaximized()
        utils.save_settings(self)
        self.topic_req_page_finished.emit(self.geometry())
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

    def get_topics(self):
        url = f'{self.user_settings['SERVER_URL']}/smartstudy/'
        headers = {'Authorization': f'Token {self.token}'}
        json = {'action':'get_topics', 'class_id':self.class_id, "course_id":self.course_id}

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
            data = response_data.get('course_topic')
            self.ui.data = data
            self.ui.refresh(self)
        except (requests.exceptions.RequestException, requests.exceptions.SSLError) as e:
            utils.popup_window('Error', f'Kérés elutasítva a szervertől: {self.user_settings['SERVER_URL']}/smartstudy/')
            self.back_to_class_page()
            return

    def available(self):
        button = self.sender()
        topic_id = int(button.objectName().split('_')[-1])
        for line in self.ui.data:
            if line["topic_id"] == topic_id:
                if line["available"] == True:
                    line.update({"available":False})
                    button.setIcon(QIcon("utils/images/not-ok-icon.png"))                    
                else:
                    line.update({"available":True})
                    button.setIcon(QIcon("utils/images/ok-icon.png"))
                return    

    def save(self):
        i = 0
        for widget in self.ui.topic_group_box.findChildren(QLineEdit):
            object_name = widget.objectName()
            text = widget.text()
            if object_name.startswith("test_task_number;"):
                i = i+1
                test_task_number_place = object_name.split(';')[0]
                try:
                    test_task_number_text = int(text)
                except:
                    test_task_number_text = 0
                self.ui.data[i-1].update({test_task_number_place:test_task_number_text})
            elif object_name.startswith("test_required_percentage;"):
                test_required_percentage_place = object_name.split(';')[0]
                try:
                    test_required_percentage_text = int(text.strip().replace("_", ""))
                except:
                    test_required_percentage_text = 0
                self.ui.data[i-1].update({test_required_percentage_place:test_required_percentage_text})

        url = f'{self.user_settings['SERVER_URL']}/smartstudy/'
        headers = {'Authorization': f'Token {self.token}'}
        json = {'action':'set_courses', 'class_id':self.class_id, "course_id":self.course_id, "course_topic":self.ui.data}

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
            self.get_topics()
        except (requests.exceptions.RequestException, requests.exceptions.SSLError) as e:
            utils.popup_window('Error', f'Kérés elutasítva a szervertől: {self.user_settings['SERVER_URL']}/smartstudy/')
            return
