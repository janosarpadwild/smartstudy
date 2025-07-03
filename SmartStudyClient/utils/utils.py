from utils.crash_report import crash_report
import os, json, sys
from PyQt6.QtWidgets import QMessageBox, QPushButton

def load_static(self):
    try:
        with open('utils/json/static.json', 'r', encoding='utf-8') as json_file:
            try:
                self.static = json.loads(json_file.read())
            except ValueError as e:
                crash_report(f'Error in {__name__}\nLoading static.json has failed!\nProgram run in {os.getcwd()}',e)
                popup_window('Error', 'Loading static.json has failed!')
                sys.exit(2)
    except FileNotFoundError as e:
        crash_report(f'Error in {__name__}\nutils/json/static.json is not found!\nProgram run in {os.getcwd()}',e)
        popup_window('Error', 'static.json is not found!')
        sys.exit(1)
    return

def load_user_settings(self):    
    try:        
        with open('utils/json/user_settings.json', 'r', encoding='utf-8') as json_file:
            try:
                self.user_settings = json.loads(json_file.read())
            except ValueError as e:
                crash_report(f'Error in {__name__}\nLoading user_settings.json has failed!\nProgram run in {os.getcwd()}',e)
                popup_window('Error', 'Loading static.json has failed!')
                sys.exit(2)
    except FileNotFoundError as e:
        crash_report(f'Error in {__name__}\nuser_settings.json is not found!\nProgram run in {os.getcwd()}',e)
        popup_window('Error', 'user_settings.json is not found!')
        sys.exit(1)
    return

def save_settings(self):
    try:        
        with open('utils/json/user_settings.json', 'w', encoding='utf-8') as json_file:
            try:
                json.dump(self.user_settings, json_file, indent=4)
            except TypeError as e:
                crash_report(f'Error in {__name__}\nWriting the updated user_settings.json has failed!\nProgram run in {os.getcwd()}',e)
                popup_window('Error', 'Writing the updated static.json has failed!')
                sys.exit(2)
    except FileNotFoundError as e:
        crash_report(f'Error in {__name__}\nuser_settings.json is not found!\nProgram run in {os.getcwd()}',e)
        popup_window('Error', 'user_settings.json is not found!')
        sys.exit(1)
    return

def popup_window(type, text):
    msg = QMessageBox()
    match type:
        case 'Error':
            msg.setIcon(QMessageBox.Icon.Critical)
            msg.setWindowTitle("Error")
        case 'Warning':
            msg.setIcon(QMessageBox.Icon.Warning)
            msg.setWindowTitle("Warning")
        case 'Information':
            msg.setIcon(QMessageBox.Icon.Information)
            msg.setWindowTitle("Information")
    msg.setText(text)        
    msg.exec()

def too_small_screen():
    message_box = QMessageBox()

    message_box.setIcon(QMessageBox.Icon.Warning)
    message_box.setWindowTitle("Warning")
    message_box.setText("A képernyő méretéhez ez a betűméret megjelenési problémákhoz vezethet. Biztos folytatja?")

    save_button = QPushButton("Igen")
    message_box.addButton(save_button, QMessageBox.ButtonRole.AcceptRole)
    cancel_button = QPushButton("Mégse")
    message_box.addButton(cancel_button, QMessageBox.ButtonRole.RejectRole)

    message_box.setDefaultButton(save_button)

    result = message_box.exec()

    if message_box.clickedButton() == save_button:
        return True
    elif message_box.clickedButton() == cancel_button:
        return False
    else:
        return False