# Form implementation generated from reading ui file 'login.ui'
#
# Created by: PyQt6 UI code generator 6.6.1
#
# WARNING: Any manual changes made to this file will be lost when pyuic6 is
# run again.  Do not edit this file unless you know what you are doing.

from PyQt6 import QtCore, QtGui, QtWidgets
from utils.validators import PASSWORD_VALIDATOR, EMAIL_VALIDATOR

class Ui_login_form(object):
    def __init__(self, static):
        super().__init__()
        self.text=static['text']
        self.smalltext=static['smalltext']
        self.button=static['button']
        self.cmd_link_btn = static['cmd_link_btn']

    def setupUi(self, login_form):
        login_form.setObjectName("login_form")
        login_form.resize(400, 330)
        login_form.setMinimumSize(QtCore.QSize(400, 330))
        login_form.setMaximumSize(QtCore.QSize(400, 330))
        login_form.setBaseSize(QtCore.QSize(0, 0))
        palette = QtGui.QPalette()
        brush = QtGui.QBrush(QtGui.QColor(131, 203, 235))
        brush.setStyle(QtCore.Qt.BrushStyle.SolidPattern)
        palette.setBrush(QtGui.QPalette.ColorGroup.Active, QtGui.QPalette.ColorRole.Button, brush)
        brush = QtGui.QBrush(QtGui.QColor(255, 255, 255))
        brush.setStyle(QtCore.Qt.BrushStyle.SolidPattern)
        palette.setBrush(QtGui.QPalette.ColorGroup.Active, QtGui.QPalette.ColorRole.Base, brush)
        brush = QtGui.QBrush(QtGui.QColor(217, 242, 208))
        brush.setStyle(QtCore.Qt.BrushStyle.SolidPattern)
        palette.setBrush(QtGui.QPalette.ColorGroup.Active, QtGui.QPalette.ColorRole.Window, brush)
        brush = QtGui.QBrush(QtGui.QColor(131, 203, 235))
        brush.setStyle(QtCore.Qt.BrushStyle.SolidPattern)
        palette.setBrush(QtGui.QPalette.ColorGroup.Inactive, QtGui.QPalette.ColorRole.Button, brush)
        brush = QtGui.QBrush(QtGui.QColor(255, 255, 255))
        brush.setStyle(QtCore.Qt.BrushStyle.SolidPattern)
        palette.setBrush(QtGui.QPalette.ColorGroup.Inactive, QtGui.QPalette.ColorRole.Base, brush)
        brush = QtGui.QBrush(QtGui.QColor(217, 242, 208))
        brush.setStyle(QtCore.Qt.BrushStyle.SolidPattern)
        palette.setBrush(QtGui.QPalette.ColorGroup.Inactive, QtGui.QPalette.ColorRole.Window, brush)
        brush = QtGui.QBrush(QtGui.QColor(131, 203, 235))
        brush.setStyle(QtCore.Qt.BrushStyle.SolidPattern)
        palette.setBrush(QtGui.QPalette.ColorGroup.Disabled, QtGui.QPalette.ColorRole.Button, brush)
        brush = QtGui.QBrush(QtGui.QColor(217, 242, 208))
        brush.setStyle(QtCore.Qt.BrushStyle.SolidPattern)
        palette.setBrush(QtGui.QPalette.ColorGroup.Disabled, QtGui.QPalette.ColorRole.Base, brush)
        brush = QtGui.QBrush(QtGui.QColor(217, 242, 208))
        brush.setStyle(QtCore.Qt.BrushStyle.SolidPattern)
        palette.setBrush(QtGui.QPalette.ColorGroup.Disabled, QtGui.QPalette.ColorRole.Window, brush)
        login_form.setPalette(palette)
        login_form.setAutoFillBackground(True)
        self.login_form_layout = QtWidgets.QFormLayout(login_form)
        self.login_form_layout.setContentsMargins(40, 40, 40, 40)
        self.login_form_layout.setHorizontalSpacing(10)
        self.login_form_layout.setVerticalSpacing(5)
        self.login_form_layout.setObjectName("login_form_layout")
        self.email_label = QtWidgets.QLabel(parent=login_form)
        font = QtGui.QFont()
        font.setPointSize(self.text)
        self.email_label.setFont(font)
        self.email_label.setStyleSheet("")
        self.email_label.setObjectName("email_label")
        self.login_form_layout.setWidget(0, QtWidgets.QFormLayout.ItemRole.LabelRole, self.email_label)
        self.email_line_edit = QtWidgets.QLineEdit(parent=login_form)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Policy.Expanding, QtWidgets.QSizePolicy.Policy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.email_line_edit.sizePolicy().hasHeightForWidth())
        self.email_line_edit.setSizePolicy(sizePolicy)
        self.email_line_edit.setMinimumSize(QtCore.QSize(0, 30))
        font = QtGui.QFont()
        font.setPointSize(self.text)
        self.email_line_edit.setFont(font)
        self.email_line_edit.setStyleSheet("border: 2px solid black;")
        self.email_line_edit.setInputMethodHints(QtCore.Qt.InputMethodHint.ImhEmailCharactersOnly)
        self.email_line_edit.setValidator(EMAIL_VALIDATOR)
        self.email_line_edit.setMaxLength(255)
        self.email_line_edit.setObjectName("email_line_edit")
        self.login_form_layout.setWidget(0, QtWidgets.QFormLayout.ItemRole.FieldRole, self.email_line_edit)
        self.password_label = QtWidgets.QLabel(parent=login_form)
        font = QtGui.QFont()
        font.setPointSize(self.text)
        self.password_label.setFont(font)
        self.password_label.setObjectName("password_label")
        self.login_form_layout.setWidget(1, QtWidgets.QFormLayout.ItemRole.LabelRole, self.password_label)
        self.password_line_edit = QtWidgets.QLineEdit(parent=login_form)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Policy.Expanding, QtWidgets.QSizePolicy.Policy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.password_line_edit.sizePolicy().hasHeightForWidth())
        self.password_line_edit.setSizePolicy(sizePolicy)
        self.password_line_edit.setMinimumSize(QtCore.QSize(0, 30))
        font = QtGui.QFont()
        font.setPointSize(self.text)
        self.password_line_edit.setFont(font)
        self.password_line_edit.setStyleSheet("border: 2px solid black;")
        self.password_line_edit.setMaxLength(50)
        self.password_line_edit.setEchoMode(QtWidgets.QLineEdit.EchoMode.Password)
        self.password_line_edit.setValidator(PASSWORD_VALIDATOR)
        self.password_line_edit.setObjectName("password_line_edit")
        self.login_form_layout.setWidget(1, QtWidgets.QFormLayout.ItemRole.FieldRole, self.password_line_edit)
        self.groupBox = QtWidgets.QGroupBox(parent=login_form)
        self.groupBox.setStyleSheet("border:none")
        self.groupBox.setTitle("")
        self.groupBox.setObjectName("groupBox")
        self.horizontalLayout = QtWidgets.QHBoxLayout(self.groupBox)
        self.horizontalLayout.setContentsMargins(0, 0, 0, 0)
        self.horizontalLayout.setObjectName("horizontalLayout")
        spacerItem = QtWidgets.QSpacerItem(81, 20, QtWidgets.QSizePolicy.Policy.Minimum, QtWidgets.QSizePolicy.Policy.Minimum)
        self.horizontalLayout.addItem(spacerItem)
        self.login_btn = QtWidgets.QPushButton(parent=self.groupBox)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Policy.Fixed, QtWidgets.QSizePolicy.Policy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.login_btn.sizePolicy().hasHeightForWidth())
        self.login_btn.setSizePolicy(sizePolicy)
        self.login_btn.setMinimumSize(QtCore.QSize(0, 40))
        palette = QtGui.QPalette()
        brush = QtGui.QBrush(QtGui.QColor(217, 242, 208))
        brush.setStyle(QtCore.Qt.BrushStyle.SolidPattern)
        palette.setBrush(QtGui.QPalette.ColorGroup.Active, QtGui.QPalette.ColorRole.Button, brush)
        brush = QtGui.QBrush(QtGui.QColor(217, 242, 208))
        brush.setStyle(QtCore.Qt.BrushStyle.SolidPattern)
        palette.setBrush(QtGui.QPalette.ColorGroup.Active, QtGui.QPalette.ColorRole.Base, brush)
        brush = QtGui.QBrush(QtGui.QColor(217, 242, 208))
        brush.setStyle(QtCore.Qt.BrushStyle.SolidPattern)
        palette.setBrush(QtGui.QPalette.ColorGroup.Active, QtGui.QPalette.ColorRole.Window, brush)
        brush = QtGui.QBrush(QtGui.QColor(217, 242, 208))
        brush.setStyle(QtCore.Qt.BrushStyle.SolidPattern)
        palette.setBrush(QtGui.QPalette.ColorGroup.Inactive, QtGui.QPalette.ColorRole.Button, brush)
        brush = QtGui.QBrush(QtGui.QColor(217, 242, 208))
        brush.setStyle(QtCore.Qt.BrushStyle.SolidPattern)
        palette.setBrush(QtGui.QPalette.ColorGroup.Inactive, QtGui.QPalette.ColorRole.Base, brush)
        brush = QtGui.QBrush(QtGui.QColor(217, 242, 208))
        brush.setStyle(QtCore.Qt.BrushStyle.SolidPattern)
        palette.setBrush(QtGui.QPalette.ColorGroup.Inactive, QtGui.QPalette.ColorRole.Window, brush)
        brush = QtGui.QBrush(QtGui.QColor(217, 242, 208))
        brush.setStyle(QtCore.Qt.BrushStyle.SolidPattern)
        palette.setBrush(QtGui.QPalette.ColorGroup.Disabled, QtGui.QPalette.ColorRole.Button, brush)
        brush = QtGui.QBrush(QtGui.QColor(217, 242, 208))
        brush.setStyle(QtCore.Qt.BrushStyle.SolidPattern)
        palette.setBrush(QtGui.QPalette.ColorGroup.Disabled, QtGui.QPalette.ColorRole.Base, brush)
        brush = QtGui.QBrush(QtGui.QColor(217, 242, 208))
        brush.setStyle(QtCore.Qt.BrushStyle.SolidPattern)
        palette.setBrush(QtGui.QPalette.ColorGroup.Disabled, QtGui.QPalette.ColorRole.Window, brush)
        self.login_btn.setPalette(palette)
        font = QtGui.QFont()
        font.setPointSize(self.button)
        self.login_btn.setFont(font)
        self.login_btn.setCursor(QtGui.QCursor(QtCore.Qt.CursorShape.PointingHandCursor))
        self.login_btn.setAutoFillBackground(False)
        self.login_btn.setStyleSheet("QPushButton {background-color: #D9F2D0; border: 2px solid black; border-radius:10; padding-left:20px;padding-right:20px;}\n"
                                    "QPushButton:hover {background-color: #55aa00; border: 2px solid black; border-radius:10; padding-left:20px;padding-right:20px;}")
        self.login_btn.setObjectName("login_btn")
        self.horizontalLayout.addWidget(self.login_btn)
        self.show_password_check_box = QtWidgets.QCheckBox(parent=self.groupBox)
        font = QtGui.QFont()
        font.setPointSize(self.smalltext)
        self.show_password_check_box.setFont(font)
        self.show_password_check_box.setObjectName("show_password_check_box")
        self.horizontalLayout.addWidget(self.show_password_check_box)
        self.login_form_layout.setWidget(2, QtWidgets.QFormLayout.ItemRole.SpanningRole, self.groupBox)
        self.forgot_password_cmd_link_btn = QtWidgets.QCommandLinkButton(parent=login_form)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Policy.Preferred, QtWidgets.QSizePolicy.Policy.Maximum)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.forgot_password_cmd_link_btn.sizePolicy().hasHeightForWidth())
        self.forgot_password_cmd_link_btn.setSizePolicy(sizePolicy)
        self.forgot_password_cmd_link_btn.setMinimumSize(QtCore.QSize(0, 30))
        self.forgot_password_cmd_link_btn.setMaximumSize(QtCore.QSize(16777215, 30))
        font = QtGui.QFont()
        font.setFamily("Segoe UI")
        font.setPointSize(self.cmd_link_btn)
        self.forgot_password_cmd_link_btn.setFont(font)
        self.forgot_password_cmd_link_btn.setCursor(QtGui.QCursor(QtCore.Qt.CursorShape.PointingHandCursor))
        self.forgot_password_cmd_link_btn.setObjectName("forgot_password_cmd_link_btn")
        icon = QtGui.QIcon('utils/images/right-arrow.png')           
        self.forgot_password_cmd_link_btn.setIcon(icon)
        self.login_form_layout.setWidget(3, QtWidgets.QFormLayout.ItemRole.SpanningRole, self.forgot_password_cmd_link_btn)
        self.change_email_cmd_link_btn = QtWidgets.QCommandLinkButton(parent=login_form)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Policy.Preferred, QtWidgets.QSizePolicy.Policy.Maximum)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.change_email_cmd_link_btn.sizePolicy().hasHeightForWidth())
        self.change_email_cmd_link_btn.setSizePolicy(sizePolicy)
        self.change_email_cmd_link_btn.setMinimumSize(QtCore.QSize(0, 30))
        self.change_email_cmd_link_btn.setMaximumSize(QtCore.QSize(16777215, 30))
        font = QtGui.QFont()
        font.setFamily("Segoe UI")
        font.setPointSize(self.cmd_link_btn)
        self.change_email_cmd_link_btn.setFont(font)
        self.change_email_cmd_link_btn.setCursor(QtGui.QCursor(QtCore.Qt.CursorShape.PointingHandCursor))
        self.change_email_cmd_link_btn.setObjectName("change_email_cmd_link_btn")
        icon = QtGui.QIcon('utils/images/right-arrow.png')           
        self.change_email_cmd_link_btn.setIcon(icon)
        self.login_form_layout.setWidget(4, QtWidgets.QFormLayout.ItemRole.SpanningRole, self.change_email_cmd_link_btn)
        self.new_server_cmd_link_btn = QtWidgets.QCommandLinkButton(parent=login_form)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Policy.Preferred, QtWidgets.QSizePolicy.Policy.Maximum)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.new_server_cmd_link_btn.sizePolicy().hasHeightForWidth())
        self.new_server_cmd_link_btn.setSizePolicy(sizePolicy)
        self.new_server_cmd_link_btn.setMinimumSize(QtCore.QSize(0, 30))
        self.new_server_cmd_link_btn.setMaximumSize(QtCore.QSize(16777215, 30))
        font = QtGui.QFont()
        font.setFamily("Segoe UI")
        font.setPointSize(self.cmd_link_btn)
        self.new_server_cmd_link_btn.setFont(font)
        self.new_server_cmd_link_btn.setCursor(QtGui.QCursor(QtCore.Qt.CursorShape.PointingHandCursor))
        self.new_server_cmd_link_btn.setLayoutDirection(QtCore.Qt.LayoutDirection.LeftToRight)
        self.new_server_cmd_link_btn.setObjectName("new_server_cmd_link_btn")
        icon = QtGui.QIcon('utils/images/right-arrow.png')           
        self.new_server_cmd_link_btn.setIcon(icon)
        self.login_form_layout.setWidget(5, QtWidgets.QFormLayout.ItemRole.SpanningRole, self.new_server_cmd_link_btn)
        self.unathorized_cmd_link_btn = QtWidgets.QCommandLinkButton(parent=login_form)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Policy.Preferred, QtWidgets.QSizePolicy.Policy.Maximum)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.unathorized_cmd_link_btn.sizePolicy().hasHeightForWidth())
        self.unathorized_cmd_link_btn.setSizePolicy(sizePolicy)
        self.unathorized_cmd_link_btn.setMinimumSize(QtCore.QSize(0, 30))
        self.unathorized_cmd_link_btn.setMaximumSize(QtCore.QSize(16777215, 30))
        font = QtGui.QFont()
        font.setFamily("Segoe UI")
        font.setPointSize(self.cmd_link_btn)
        self.unathorized_cmd_link_btn.setFont(font)
        self.unathorized_cmd_link_btn.setCursor(QtGui.QCursor(QtCore.Qt.CursorShape.PointingHandCursor))
        self.unathorized_cmd_link_btn.setStyleSheet("")
        self.unathorized_cmd_link_btn.setObjectName("unathorized_cmd_link_btn")
        icon = QtGui.QIcon('utils/images/right-arrow.png')           
        self.unathorized_cmd_link_btn.setIcon(icon)
        self.login_form_layout.setWidget(6, QtWidgets.QFormLayout.ItemRole.SpanningRole, self.unathorized_cmd_link_btn)

        self.retranslateUi(login_form)
        QtCore.QMetaObject.connectSlotsByName(login_form)

    def retranslateUi(self, login_form):
        _translate = QtCore.QCoreApplication.translate
        login_form.setWindowTitle(_translate("login_form", "Bejelentkezés"))
        login_form.setWindowIcon(QtGui.QIcon("utils/images/window-icon.png"))
        self.email_label.setText(_translate("login_form", "E-mail cím:"))
        self.password_label.setText(_translate("login_form", "Jelszó:"))
        self.login_btn.setText(_translate("login_form", "Belépés"))
        self.show_password_check_box.setText(_translate("login_form", "Jelszó megjelenítése"))
        self.forgot_password_cmd_link_btn.setText(_translate("login_form", "Elfelejtett jelszó"))
        self.change_email_cmd_link_btn.setText(_translate("login_form", "E-mail cím cseréje"))
        self.new_server_cmd_link_btn.setText(_translate("login_form", "Új szerver beállítása"))
        self.unathorized_cmd_link_btn.setText(_translate("login_form", "Visszaélés bejelentése"))
