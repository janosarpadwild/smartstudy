import requests
from PyQt6.QtWidgets import QWidget
from PyQt6.QtCore import pyqtSignal, QRect
from PyQt6.QtGui import QGuiApplication
from student.student_ui.task_page_form import Ui_task_page
from utils import utils

class TaskPage(QWidget):
    task_page_finished = pyqtSignal(QRect)
    def __init__(self, token, subtopic_name, subtopic_id, test, topic_id, topic_name, course_id, geometry, session):
        super().__init__()
        # Loading view settings and user settings to self.static and self.user_settings
        utils.load_static(self)
        utils.load_user_settings(self)
        self.session=session
        self.token = token
        self.subtopic_name = subtopic_name
        self.subtopic_id = subtopic_id
        self.test = test
        self.topic_id = topic_id
        self.topic_name = topic_name
        self.course_id = course_id
        self.index=0
        match self.user_settings['font-size']:
            case "small":
                self.window_size_index = 0
            case "medium":
                self.window_size_index = 1
            case "big":
                self.window_size_index = 2
        # Setup view
        self.ui = Ui_task_page(self.static['user'][self.user_settings['font-size']])

        self.ui.setupUi(self)
        if test:
            self.ui.task_label.setText('Teszt feladat')

        self.get_task()
        self.setGeometry(geometry)
        self.resize_window()

        self.ui.font_size_combo_box.currentIndexChanged.connect(self.resize_window)
        self.ui.back_to_topics_cmd_link_btn.clicked.connect(self.back_to_subtopic_main_page)

        # Show task page
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
        self.ui.task(self)

    def back_to_subtopic_main_page(self):
        self.user_settings['maximized'] = self.isMaximized()
        utils.save_settings(self)
        self.task_page_finished.emit(self.geometry())
        self.close()

    def get_task(self):
        url = f'{self.user_settings['SERVER_URL']}/smartstudy/'
        headers = {'Authorization': f'Token {self.token}'}
        json = {}
        if self.test:
            json = {'action':'get_test_tasks', 'course_id':self.course_id, 'topic_id':self.topic_id}
        else:
            json = {'action':'get_practise_tasks', 'course_id':self.course_id, 'topic_id':self.topic_id, 'subtopic_id':self.subtopic_id}

        try:
            if url.startswith('https://127.0.0.1'):
                # Localhost SSL verification
                response = self.session.get(url, headers=headers, json=json)                
            else:
                response = self.session.get(url, headers=headers, json=json, verify=True)
            response_data = response.json()
            data = response_data.get('tasks')
            self.ui.data = data
            self.ui.task(self)
        except (requests.exceptions.RequestException, requests.exceptions.SSLError) as e:
            utils.popup_window('Error', f'Kérés elutasítva a szervertől: {self.user_settings['SERVER_URL']}/smartstudy/')
            self.back_to_subtopic_main_page()
        
    def send_enable(self):
        if self.ui.answer_line_edit.text()=="":
            self.ui.answer_btn.setEnabled(False)
        else:
            self.ui.answer_btn.setEnabled(True)

    def send(self):
        if self.ui.answer_btn.text() == "Küldés":
            try:
                self.next_task()  
                self.ui.send_btn_text()          
            except:
                return
        else:
            if self.index+1<len(self.ui.data):
                self.index += 1
                self.ui.task(self)
            else:
                self.back_to_subtopic_main_page()
        

    def next_task(self):
        answer = round(float(self.ui.answer_line_edit.text()), 3)
        if self.test:
            self.subtopic_id = -1
        print('shit')
        url = f'{self.user_settings['SERVER_URL']}/smartstudy/'
        headers = {'Authorization': f'Token {self.token}'}
        json = {'action':'task_answer', 'course_id':int(self.course_id), 'topic_id':int(self.topic_id), 'subtopic_id':self.subtopic_id, 'task_id':int(self.ui.data[self.index]['task_progress_id']), 'test':self.test, "answer":answer}
        print(json)
        try:
            print('try')
            if url.startswith('https://127.0.0.1'):
                # Localhost SSL verification
                response = self.session.post(url, headers=headers, json=json)                
            else:
                response = self.session.post(url, headers=headers, json=json, verify=True)
            response_data = response.json()
            error = response_data.get('error')
            if error != None:
                utils.popup_window('Error', error)
        except (requests.exceptions.RequestException, requests.exceptions.SSLError) as e:
            utils.popup_window('Error', f'Kérés elutasítva a szervertől: {self.user_settings['SERVER_URL']}/smartstudy/')
            raise(Exception)