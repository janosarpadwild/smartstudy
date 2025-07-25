# Form implementation generated from reading ui file 'teacher_main_page.ui'
#
# Created by: PyQt6 UI code generator 6.6.1
#
# WARNING: Any manual changes made to this file will be lost when pyuic6 is
# run again.  Do not edit this file unless you know what you are doing.


from PyQt6 import QtCore, QtGui, QtWidgets


class Ui_teacher_main_page(object):
    def __init__(self, static):
        super().__init__()
        self.static = static
        self.class_data = []
        self.subject_data = []
        
    def screen_size(self, teacher_main_page):
        screen_geometry = QtWidgets.QApplication.primaryScreen().availableGeometry()
        width = screen_geometry.width()
        height = screen_geometry.height()
        if width >= self.static["window-size"]["width"] and height >= self.static["window-size"]["height"]:
            teacher_main_page.setMinimumSize(QtCore.QSize(self.static["window-size"]["width"], self.static["window-size"]["height"]))
            qr=teacher_main_page.frameGeometry()           
            cp=QtGui.QGuiApplication.primaryScreen().availableGeometry().center()
            qr.moveCenter(cp)
            teacher_main_page.move(qr.topLeft())
        else:
            teacher_main_page.setMinimumSize(QtCore.QSize(width, height))
            qr=teacher_main_page.frameGeometry()           
            cp=QtGui.QGuiApplication.primaryScreen().availableGeometry().center()
            qr.moveCenter(cp)
            teacher_main_page.move(qr.topLeft())
        
    def subjects(self):
        self.subject_combo_box.clear()
        self.subject_combo_box.addItem("")
        self.subject_combo_box.setItemText(0, "")
        index = 1
        for subject in [list(line.keys())[0] for line in self.subject_data]:
            self.subject_combo_box.addItem("")
            self.subject_combo_box.setItemText(index, subject)
            index+=1

    def refresh(self, teacher_main_page):
        self.teacher_main_page_vertical_layout.setSpacing(self.static["layout-spacing"])
        self.menu_horizontal_layout.setContentsMargins(self.static["menu"]["layout"]["left"], self.static["menu"]["layout"]["top"], self.static["menu"]["layout"]["right"], self.static["menu"]["layout"]["bottom"])

        font = QtGui.QFont()
        font.setPointSize(self.static["font-sizes"]["title"])
        self.menu_label.setFont(font)

        font = QtGui.QFont()
        font.setPointSize(self.static["font-sizes"]["size-menu"])
        self.font_size_combo_box.setFont(font)

        self.logout_cmd_link_btn.setMinimumSize(QtCore.QSize(self.static["menu"]["backtrack-width"], 45))
        self.logout_cmd_link_btn.setMaximumSize(QtCore.QSize(self.static["menu"]["backtrack-width"], 45))

        font = QtGui.QFont()
        font.setFamily("Segoe UI")
        font.setPointSize(self.static["font-sizes"]["text"])
        self.logout_cmd_link_btn.setFont(font)

        font = QtGui.QFont()
        font.setPointSize(self.static["font-sizes"]["text"])
        self.subject_combo_box.setFont(font)

        font = QtGui.QFont()
        font.setPointSize(self.static["font-sizes"]["subtitle"])
        self.teacher_name_label.setFont(font)

        font = QtGui.QFont()
        font.setPointSize(self.static["font-sizes"]["text"])
        self.course_subject_label.setFont(font)

        self.teacher_name_label.setStyleSheet(f"margin-left:{self.static["subtitle-margin-left"]}px;margin-top:10px; margin-bottom:10px;")

        font = QtGui.QFont()
        font.setPointSize(self.static["font-sizes"]["subtitle"])
        self.tabWidget.setFont(font)

        self.class_list(teacher_main_page)
        self.subject_list(teacher_main_page)

        self.course_subject_label.setMinimumHeight(self.static["topic"]["height"]-10)

        self.subject_combo_box.setMinimumSize(QtCore.QSize(self.static["topic"]["small-width"], self.static["topic"]["height"]-10))

        QtCore.QMetaObject.connectSlotsByName(teacher_main_page)

    def class_list(self, teacher_main_page):        
        if self.class_data == []:
            return
    
        self.class_scroll_area_vertical_layout.removeWidget(self.class_list_group_box)

        self.class_list_group_box = QtWidgets.QGroupBox(parent=self.class_scroll_area_contents)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Policy.Expanding, QtWidgets.QSizePolicy.Policy.Expanding)
        self.class_list_group_box.setSizePolicy(sizePolicy)
        self.class_list_group_box.setTitle("")
        self.class_list_group_box.setObjectName("class_list_group_box")
        self.class_list_vertical_layout = QtWidgets.QHBoxLayout(self.class_list_group_box)
        self.class_list_vertical_layout.setContentsMargins(0, 10, 0, 0)
        self.class_list_vertical_layout.setSpacing(5)
        self.class_list_vertical_layout.setObjectName("class_list_vertical_layout")

        spacerItem7 = QtWidgets.QSpacerItem(0, 20, QtWidgets.QSizePolicy.Policy.Expanding, QtWidgets.QSizePolicy.Policy.Minimum)
        self.class_list_vertical_layout.addItem(spacerItem7)

        self.class_name_group_box = QtWidgets.QGroupBox(parent=self.class_list_group_box)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Policy.Maximum, QtWidgets.QSizePolicy.Policy.Preferred)
        sizePolicy.setHeightForWidth(self.class_name_group_box.sizePolicy().hasHeightForWidth())
        self.class_name_group_box.setSizePolicy(sizePolicy)
        self.class_name_group_box.setTitle("")
        self.class_name_group_box.setObjectName("class_name_group_box")
        self.class_name_form_layout = QtWidgets.QFormLayout(self.class_name_group_box)
        self.class_name_form_layout.setContentsMargins(0, 0, 0, 0)
        self.class_name_form_layout.setHorizontalSpacing(0)
        self.class_name_form_layout.setVerticalSpacing(5)
        self.class_name_form_layout.setObjectName("class_name_form_layout")

        self.class_details_group_box = QtWidgets.QGroupBox(parent=self.class_list_group_box)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Policy.Maximum, QtWidgets.QSizePolicy.Policy.Preferred)
        sizePolicy.setHeightForWidth(self.class_details_group_box.sizePolicy().hasHeightForWidth())
        self.class_details_group_box.setSizePolicy(sizePolicy)
        self.class_details_group_box.setTitle("")
        self.class_details_group_box.setObjectName("class_details_group_box")
        self.class_details_form_layout = QtWidgets.QFormLayout(self.class_details_group_box)
        self.class_details_form_layout.setContentsMargins(0, 0, 0, 0)
        self.class_details_form_layout.setHorizontalSpacing(0)
        self.class_details_form_layout.setVerticalSpacing(5)
        self.class_details_form_layout.setObjectName("class_details_form_layout")

        index = 0
        for line in self.class_data:
            class_label = QtWidgets.QLabel(line["class_name"], parent=self.class_name_group_box)
            sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Policy.Preferred, QtWidgets.QSizePolicy.Policy.Fixed)
            sizePolicy.setHeightForWidth(class_label.sizePolicy().hasHeightForWidth())
            class_label.setSizePolicy(sizePolicy)
            class_label.setMinimumSize(QtCore.QSize(self.static["topic"]["height"], self.static["topic"]["height"]))
            class_label.setMaximumSize(QtCore.QSize(16777215, self.static["topic"]["height"]))
            font = QtGui.QFont()
            font.setPointSize(self.static["font-sizes"]["text"])
            class_label.setFont(font)
            class_label.setObjectName(f"class_label_{line["id"]}")
            self.class_name_form_layout.setWidget(index, QtWidgets.QFormLayout.ItemRole.LabelRole, class_label)

            class_btn = QtWidgets.QPushButton("Előrehaladás megtekintése", parent=self.class_details_group_box)
            sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Policy.Preferred, QtWidgets.QSizePolicy.Policy.Fixed)
            sizePolicy.setHeightForWidth(class_btn.sizePolicy().hasHeightForWidth())
            class_btn.setSizePolicy(sizePolicy)
            class_btn.setMinimumSize(QtCore.QSize(self.static["topic"]["desc-width"], self.static["topic"]["height"]))
            class_btn.setMaximumSize(QtCore.QSize(16777215, self.static["topic"]["height"]))
            font = QtGui.QFont()
            font.setPointSize(self.static["font-sizes"]["text"])
            class_btn.setFont(font)
            class_btn.setCursor(QtGui.QCursor(QtCore.Qt.CursorShape.PointingHandCursor))
            class_btn.setStyleSheet("QPushButton {background-color: #D9F2D0; border: 2px solid black; border-radius:10; padding-left:20px;padding-right:20px;}\n"
                                        "QPushButton:hover {background-color: #55aa00; border: 2px solid black; border-radius:10; padding-left:20px;padding-right:20px;}")
            class_btn.setObjectName(f"class_btn_{line["class_name"]}_{line["id"]}")
            self.class_details_form_layout.setWidget(index, QtWidgets.QFormLayout.ItemRole.LabelRole, class_btn)
            class_btn.clicked.connect(teacher_main_page.get_class)

            index+=1
        
        self.class_list_vertical_layout.addWidget(self.class_name_group_box)

        self.class_list_vertical_layout.addWidget(self.class_details_group_box)

        spacerItem8 = QtWidgets.QSpacerItem(0, 20, QtWidgets.QSizePolicy.Policy.Expanding, QtWidgets.QSizePolicy.Policy.Minimum)
        self.class_list_vertical_layout.addItem(spacerItem8)

        self.class_scroll_area_vertical_layout.addWidget(self.class_list_group_box)

    def subject_list(self, teacher_main_page):
        self.topic_list_vertical_layout.removeWidget(self.topic_list_group_box)

        self.topic_list_group_box = QtWidgets.QGroupBox(parent=self.topic_list_scroll_area_content)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Policy.Expanding, QtWidgets.QSizePolicy.Policy.Expanding)
        self.topic_list_group_box.setSizePolicy(sizePolicy)
        self.topic_list_group_box.setTitle("")
        self.topic_list_group_box.setObjectName("topic_list_group_box")

        self.topic_list_horizontal_layout = QtWidgets.QHBoxLayout(self.topic_list_group_box)
        self.topic_list_horizontal_layout.setContentsMargins(self.static["menu"]["layout"]["left"], self.static["menu"]["layout"]["top"], self.static["menu"]["layout"]["right"], self.static["menu"]["layout"]["bottom"])
        self.topic_list_horizontal_layout.setSpacing(5)
        self.topic_list_horizontal_layout.setObjectName("topic_list_horizontal_layout")
        self.topic_list_horizontal_layout.setAlignment(QtCore.Qt.AlignmentFlag.AlignHCenter|QtCore.Qt.AlignmentFlag.AlignTop)

        self.topic_list_vertical_layout.addWidget(self.topic_list_group_box)

        if self.subject_data == [] or self.subject_combo_box.currentText() == "":            
            return 
        
        
        match teacher_main_page.window_size_index:
            case 0:
                wwidth = 700
            case 1:
                wwidth = 1580
            case 2:
                wwidth = 1900

        maximum_length = 0
        for line in self.subject_data[self.subject_combo_box.currentIndex()-1][self.subject_combo_box.currentText()]:
            current_length = (len(line["topic_name"])+len(line["description"]))*self.static["font-sizes"]["text"]*0.59
            if current_length>maximum_length:
                maximum_length = current_length
        maximum_length = int(maximum_length+(self.static["menu"]["layout"]["left"]+self.static["menu"]["layout"]["right"]+5+155)*0.59)#
        maximum_size = wwidth-self.static["menu"]["layout"]["left"]-self.static["menu"]["layout"]["right"]-10
        if maximum_length > maximum_size:            
            maximum_length = maximum_size

        self.topic_detail_group_box = QtWidgets.QGroupBox(parent=self.topic_list_group_box)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Policy.Maximum, QtWidgets.QSizePolicy.Policy.Maximum)
        self.topic_detail_group_box.setSizePolicy(sizePolicy)        
        self.topic_detail_group_box.setMinimumSize(QtCore.QSize(maximum_length, self.static["topic"]["height"]))
        self.topic_detail_group_box.setTitle("")
        self.topic_detail_group_box.setObjectName("topic_detail_group_box")        

        self.topic_detail_grid_layout = QtWidgets.QGridLayout(self.topic_detail_group_box)
        self.topic_detail_grid_layout.setContentsMargins(0, 0, 0, 0)
        self.topic_detail_grid_layout.setSpacing(5)
        self.topic_detail_grid_layout.setObjectName("topic_detail_grid_layout")

        self.topic_list_horizontal_layout.addWidget(self.topic_detail_group_box)

        index = 0
        for line in self.subject_data[self.subject_combo_box.currentIndex()-1][self.subject_combo_box.currentText()]:
            topic_title_btn = QtWidgets.QPushButton(line["topic_name"], parent=self.topic_detail_group_box)
            sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Policy.Minimum, QtWidgets.QSizePolicy.Policy.Minimum)
            topic_title_btn.setSizePolicy(sizePolicy)
            topic_title_btn.setMinimumHeight(self.static["topic"]["height"])
            font = QtGui.QFont()
            font.setPointSize(self.static["font-sizes"]["text"])
            topic_title_btn.setFont(font)
            topic_title_btn.setCursor(QtGui.QCursor(QtCore.Qt.CursorShape.PointingHandCursor))
            topic_title_btn.setStyleSheet("QPushButton {background-color: #D9F2D0; border: 2px solid black; border-radius:10; padding-left:20px;padding-right:20px;}\n"
                                            "QPushButton:hover {background-color: #55aa00; border: 2px solid black; border-radius:10; padding-left:20px;padding-right:20px;}")
            topic_title_btn.setObjectName(f"topic_title_btn_{line['id']}")
            self.topic_detail_grid_layout.addWidget(topic_title_btn, index, 0, 1, 1, QtCore.Qt.AlignmentFlag.AlignVCenter)
            topic_title_btn.clicked.connect(teacher_main_page.get_subtopics)
            
            topic_desc_label = QtWidgets.QLabel(line["description"], parent=self.topic_detail_group_box)
            sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Policy.MinimumExpanding, QtWidgets.QSizePolicy.Policy.Minimum)
            topic_desc_label.setSizePolicy(sizePolicy)
            topic_desc_label.setMinimumHeight(self.static["topic"]["height"])
            font = QtGui.QFont()
            font.setPointSize(self.static["font-sizes"]["text"])
            topic_desc_label.setFont(font)
            topic_desc_label.setStyleSheet("background-color: #D9F2D0; border: 2px solid white; border-radius:10; padding-left:20px;padding-right:20px")
            topic_desc_label.setWordWrap(True)
            topic_desc_label.setObjectName(f"topic_desc_label_{line["id"]}")
            self.topic_detail_grid_layout.addWidget(topic_desc_label, index, 1, 1, 1, QtCore.Qt.AlignmentFlag.AlignVCenter)
            index+=1

    def setupUi(self, teacher_main_page):
        teacher_main_page.setObjectName("teacher_main_page")
        teacher_main_page.resize(720, 480)
        teacher_main_page.setMinimumSize(QtCore.QSize(720, 480))
        palette = QtGui.QPalette()
        brush = QtGui.QBrush(QtGui.QColor(217, 242, 208))
        brush.setStyle(QtCore.Qt.BrushStyle.SolidPattern)
        palette.setBrush(QtGui.QPalette.ColorGroup.Active, QtGui.QPalette.ColorRole.Button, brush)
        brush = QtGui.QBrush(QtGui.QColor(255, 255, 255))
        brush.setStyle(QtCore.Qt.BrushStyle.SolidPattern)
        palette.setBrush(QtGui.QPalette.ColorGroup.Active, QtGui.QPalette.ColorRole.Base, brush)
        brush = QtGui.QBrush(QtGui.QColor(131, 203, 235))
        brush.setStyle(QtCore.Qt.BrushStyle.SolidPattern)
        palette.setBrush(QtGui.QPalette.ColorGroup.Active, QtGui.QPalette.ColorRole.Window, brush)
        brush = QtGui.QBrush(QtGui.QColor(217, 242, 208))
        brush.setStyle(QtCore.Qt.BrushStyle.SolidPattern)
        palette.setBrush(QtGui.QPalette.ColorGroup.Inactive, QtGui.QPalette.ColorRole.Button, brush)
        brush = QtGui.QBrush(QtGui.QColor(255, 255, 255))
        brush.setStyle(QtCore.Qt.BrushStyle.SolidPattern)
        palette.setBrush(QtGui.QPalette.ColorGroup.Inactive, QtGui.QPalette.ColorRole.Base, brush)
        brush = QtGui.QBrush(QtGui.QColor(131, 203, 235))
        brush.setStyle(QtCore.Qt.BrushStyle.SolidPattern)
        palette.setBrush(QtGui.QPalette.ColorGroup.Inactive, QtGui.QPalette.ColorRole.Window, brush)
        brush = QtGui.QBrush(QtGui.QColor(217, 242, 208))
        brush.setStyle(QtCore.Qt.BrushStyle.SolidPattern)
        palette.setBrush(QtGui.QPalette.ColorGroup.Disabled, QtGui.QPalette.ColorRole.Button, brush)
        brush = QtGui.QBrush(QtGui.QColor(131, 203, 235))
        brush.setStyle(QtCore.Qt.BrushStyle.SolidPattern)
        palette.setBrush(QtGui.QPalette.ColorGroup.Disabled, QtGui.QPalette.ColorRole.Base, brush)
        brush = QtGui.QBrush(QtGui.QColor(131, 203, 235))
        brush.setStyle(QtCore.Qt.BrushStyle.SolidPattern)
        palette.setBrush(QtGui.QPalette.ColorGroup.Disabled, QtGui.QPalette.ColorRole.Window, brush)
        teacher_main_page.setPalette(palette)

        self.teacher_main_page_vertical_layout = QtWidgets.QVBoxLayout(teacher_main_page)
        self.teacher_main_page_vertical_layout.setContentsMargins(0, 0, 0, 0)
        self.teacher_main_page_vertical_layout.setSpacing(self.static["layout-spacing"])
        self.teacher_main_page_vertical_layout.setObjectName("teacher_main_page_vertical_layout")

        self.menu_group_box = QtWidgets.QGroupBox(parent=teacher_main_page)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Policy.Expanding, QtWidgets.QSizePolicy.Policy.Preferred)
        sizePolicy.setHeightForWidth(self.menu_group_box.sizePolicy().hasHeightForWidth())
        self.menu_group_box.setSizePolicy(sizePolicy)
        self.menu_group_box.setMinimumSize(QtCore.QSize(0, 50))
        palette = QtGui.QPalette()
        brush = QtGui.QBrush(QtGui.QColor(255, 255, 255))
        brush.setStyle(QtCore.Qt.BrushStyle.SolidPattern)
        palette.setBrush(QtGui.QPalette.ColorGroup.Active, QtGui.QPalette.ColorRole.Base, brush)
        brush = QtGui.QBrush(QtGui.QColor(255, 255, 255))
        brush.setStyle(QtCore.Qt.BrushStyle.SolidPattern)
        palette.setBrush(QtGui.QPalette.ColorGroup.Active, QtGui.QPalette.ColorRole.Window, brush)
        brush = QtGui.QBrush(QtGui.QColor(255, 255, 255))
        brush.setStyle(QtCore.Qt.BrushStyle.SolidPattern)
        palette.setBrush(QtGui.QPalette.ColorGroup.Inactive, QtGui.QPalette.ColorRole.Base, brush)
        brush = QtGui.QBrush(QtGui.QColor(255, 255, 255))
        brush.setStyle(QtCore.Qt.BrushStyle.SolidPattern)
        palette.setBrush(QtGui.QPalette.ColorGroup.Inactive, QtGui.QPalette.ColorRole.Window, brush)
        brush = QtGui.QBrush(QtGui.QColor(255, 255, 255))
        brush.setStyle(QtCore.Qt.BrushStyle.SolidPattern)
        palette.setBrush(QtGui.QPalette.ColorGroup.Disabled, QtGui.QPalette.ColorRole.Base, brush)
        brush = QtGui.QBrush(QtGui.QColor(255, 255, 255))
        brush.setStyle(QtCore.Qt.BrushStyle.SolidPattern)
        palette.setBrush(QtGui.QPalette.ColorGroup.Disabled, QtGui.QPalette.ColorRole.Window, brush)
        self.menu_group_box.setPalette(palette)
        self.menu_group_box.setAutoFillBackground(True)
        self.menu_group_box.setStyleSheet("")
        self.menu_group_box.setTitle("")
        self.menu_group_box.setObjectName("menu_group_box")

        self.menu_horizontal_layout = QtWidgets.QHBoxLayout(self.menu_group_box)
        self.menu_horizontal_layout.setContentsMargins(self.static["menu"]["layout"]["left"], self.static["menu"]["layout"]["top"], self.static["menu"]["layout"]["right"], self.static["menu"]["layout"]["bottom"])
        self.menu_horizontal_layout.setObjectName("menu_horizontal_layout")

        self.menu_label = QtWidgets.QLabel(parent=self.menu_group_box)
        font = QtGui.QFont()
        font.setPointSize(self.static["font-sizes"]["title"])
        self.menu_label.setFont(font)
        self.menu_label.setObjectName("menu_label")
        self.menu_horizontal_layout.addWidget(self.menu_label)

        spacerItem = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Policy.Expanding, QtWidgets.QSizePolicy.Policy.Minimum)
        self.menu_horizontal_layout.addItem(spacerItem)

        self.font_size_combo_box = QtWidgets.QComboBox(parent=self.menu_group_box)
        self.font_size_combo_box.setMinimumSize(QtCore.QSize(0, 30))
        font = QtGui.QFont()
        font.setPointSize(self.static["font-sizes"]["size-menu"])
        self.font_size_combo_box.setFont(font)
        self.font_size_combo_box.setCursor(QtGui.QCursor(QtCore.Qt.CursorShape.PointingHandCursor))
        self.font_size_combo_box.setStyleSheet("")
        self.font_size_combo_box.setSizeAdjustPolicy(QtWidgets.QComboBox.SizeAdjustPolicy.AdjustToContents)
        self.font_size_combo_box.setObjectName("font_size_combo_box")
        self.font_size_combo_box.addItem("")
        self.font_size_combo_box.addItem("")
        self.font_size_combo_box.addItem("")
        self.menu_horizontal_layout.addWidget(self.font_size_combo_box)

        self.logout_cmd_link_btn = QtWidgets.QCommandLinkButton(parent=self.menu_group_box)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Policy.Preferred, QtWidgets.QSizePolicy.Policy.Preferred)
        #sizePolicy.setHeightForWidth(self.logout_cmd_link_btn.sizePolicy().hasHeightForWidth())
        self.logout_cmd_link_btn.setSizePolicy(sizePolicy)
        self.logout_cmd_link_btn.setMinimumSize(QtCore.QSize(self.static["menu"]["backtrack-width"], 45))
        self.logout_cmd_link_btn.setMaximumSize(QtCore.QSize(self.static["menu"]["backtrack-width"], 45))
        font = QtGui.QFont()
        font.setFamily("Segoe UI")
        font.setPointSize(self.static["font-sizes"]["text"])
        self.logout_cmd_link_btn.setFont(font)
        self.logout_cmd_link_btn.setCursor(QtGui.QCursor(QtCore.Qt.CursorShape.PointingHandCursor))
        self.logout_cmd_link_btn.setObjectName("logout_cmd_link_btn")
        icon = QtGui.QIcon('utils/images/left-arrow.png')           
        self.logout_cmd_link_btn.setIcon(icon)
        self.menu_horizontal_layout.addWidget(self.logout_cmd_link_btn)
        self.teacher_main_page_vertical_layout.addWidget(self.menu_group_box)

        self.teacher_name_label = QtWidgets.QLabel(parent=teacher_main_page)
        font = QtGui.QFont()
        font.setPointSize(self.static["font-sizes"]["subtitle"])
        self.teacher_name_label.setFont(font)
        self.teacher_name_label.setStyleSheet(f"margin-left:{self.static["subtitle-margin-left"]}px;margin-top:10px; margin-bottom:10px;")
        self.teacher_name_label.setObjectName("teacher_name_label")
        self.teacher_main_page_vertical_layout.addWidget(self.teacher_name_label)

        self.tabWidget = QtWidgets.QTabWidget(parent=teacher_main_page)
        font = QtGui.QFont()
        font.setPointSize(self.static["font-sizes"]["subtitle"])
        self.tabWidget.setFont(font)
        self.tabWidget.setObjectName("tabWidget")

        self.class_tab = QtWidgets.QWidget()
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Policy.Expanding, QtWidgets.QSizePolicy.Policy.Expanding)
        #sizePolicy.setHeightForWidth(self.class_tab.sizePolicy().hasHeightForWidth())
        self.class_tab.setSizePolicy(sizePolicy)
        self.class_tab.setObjectName("class_tab")

        self.class_tab_vertical_layout = QtWidgets.QVBoxLayout(self.class_tab)
        self.class_tab_vertical_layout.setContentsMargins(0, 0, 0, 0)
        self.class_tab_vertical_layout.setSpacing(0)
        self.class_tab_vertical_layout.setObjectName("class_tab_vertical_layout")

        self.class_scroll_area = QtWidgets.QScrollArea(parent=self.class_tab)
        self.class_scroll_area.setStyleSheet("border:none; background-color:#83cbeb")
        self.class_scroll_area.setWidgetResizable(True)
        self.class_scroll_area.setObjectName("class_scroll_area")

        self.class_scroll_area_contents = QtWidgets.QWidget()
        self.class_scroll_area_contents.setGeometry(QtCore.QRect(0, 0, 714, 312))
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Policy.Expanding, QtWidgets.QSizePolicy.Policy.Expanding)
        #sizePolicy.setHeightForWidth(self.class_scroll_area_contents.sizePolicy().hasHeightForWidth())
        self.class_scroll_area_contents.setSizePolicy(sizePolicy)
        self.class_scroll_area_contents.setObjectName("class_scroll_area_contents")
        self.class_scroll_area_vertical_layout = QtWidgets.QVBoxLayout(self.class_scroll_area_contents)
        self.class_scroll_area_vertical_layout.setContentsMargins(0, 0, 0, 0)
        self.class_scroll_area_vertical_layout.setSpacing(0)
        self.class_scroll_area_vertical_layout.setObjectName("class_scroll_area_vertical_layout")

        self.class_list_group_box = QtWidgets.QGroupBox(parent=self.class_scroll_area_contents)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Policy.Expanding, QtWidgets.QSizePolicy.Policy.Expanding)
        #sizePolicy.setHeightForWidth(self.class_list_group_box.sizePolicy().hasHeightForWidth())
        self.class_list_group_box.setSizePolicy(sizePolicy)
        self.class_list_group_box.setTitle("")
        self.class_list_group_box.setObjectName("class_list_group_box")

        self.class_list_form_layout = QtWidgets.QFormLayout(self.class_list_group_box)
        self.class_list_form_layout.setContentsMargins(0, 10, 0, 0)
        self.class_list_form_layout.setHorizontalSpacing(0)
        self.class_list_form_layout.setVerticalSpacing(5)
        self.class_list_form_layout.setObjectName("class_list_form_layout")

        self.class_scroll_area_vertical_layout.addWidget(self.class_list_group_box)

        self.class_scroll_area.setWidget(self.class_scroll_area_contents)
        self.class_tab_vertical_layout.addWidget(self.class_scroll_area)
        self.tabWidget.addTab(self.class_tab, "")

        #new tab------------------

        self.topic_tab = QtWidgets.QWidget()
        self.topic_tab.setObjectName("topic_tab")

        self.topic_tab_vertical_layout = QtWidgets.QVBoxLayout(self.topic_tab)
        self.topic_tab_vertical_layout.setContentsMargins(0, 0, 0, 0)
        self.topic_tab_vertical_layout.setSpacing(0)
        self.topic_tab_vertical_layout.setObjectName("topic_tab_vertical_layout")

        self.topic_list_scroll_area = QtWidgets.QScrollArea(parent=self.topic_tab)
        palette = QtGui.QPalette()
        brush = QtGui.QBrush(QtGui.QColor(131, 203, 235))
        brush.setStyle(QtCore.Qt.BrushStyle.SolidPattern)
        palette.setBrush(QtGui.QPalette.ColorGroup.Active, QtGui.QPalette.ColorRole.Button, brush)
        brush = QtGui.QBrush(QtGui.QColor(131, 203, 235))
        brush.setStyle(QtCore.Qt.BrushStyle.SolidPattern)
        palette.setBrush(QtGui.QPalette.ColorGroup.Active, QtGui.QPalette.ColorRole.Base, brush)
        brush = QtGui.QBrush(QtGui.QColor(131, 203, 235))
        brush.setStyle(QtCore.Qt.BrushStyle.SolidPattern)
        palette.setBrush(QtGui.QPalette.ColorGroup.Active, QtGui.QPalette.ColorRole.Window, brush)
        brush = QtGui.QBrush(QtGui.QColor(131, 203, 235))
        brush.setStyle(QtCore.Qt.BrushStyle.SolidPattern)
        palette.setBrush(QtGui.QPalette.ColorGroup.Inactive, QtGui.QPalette.ColorRole.Button, brush)
        brush = QtGui.QBrush(QtGui.QColor(131, 203, 235))
        brush.setStyle(QtCore.Qt.BrushStyle.SolidPattern)
        palette.setBrush(QtGui.QPalette.ColorGroup.Inactive, QtGui.QPalette.ColorRole.Base, brush)
        brush = QtGui.QBrush(QtGui.QColor(131, 203, 235))
        brush.setStyle(QtCore.Qt.BrushStyle.SolidPattern)
        palette.setBrush(QtGui.QPalette.ColorGroup.Inactive, QtGui.QPalette.ColorRole.Window, brush)
        brush = QtGui.QBrush(QtGui.QColor(131, 203, 235))
        brush.setStyle(QtCore.Qt.BrushStyle.SolidPattern)
        palette.setBrush(QtGui.QPalette.ColorGroup.Disabled, QtGui.QPalette.ColorRole.Button, brush)
        brush = QtGui.QBrush(QtGui.QColor(131, 203, 235))
        brush.setStyle(QtCore.Qt.BrushStyle.SolidPattern)
        palette.setBrush(QtGui.QPalette.ColorGroup.Disabled, QtGui.QPalette.ColorRole.Base, brush)
        brush = QtGui.QBrush(QtGui.QColor(131, 203, 235))
        brush.setStyle(QtCore.Qt.BrushStyle.SolidPattern)
        palette.setBrush(QtGui.QPalette.ColorGroup.Disabled, QtGui.QPalette.ColorRole.Window, brush)
        self.topic_list_scroll_area.setPalette(palette)
        self.topic_list_scroll_area.setStyleSheet("border:none; background-color:#83cbeb")
        self.topic_list_scroll_area.setWidgetResizable(True)
        self.topic_list_scroll_area.setObjectName("topic_list_scroll_area")

        self.topic_list_scroll_area_content = QtWidgets.QWidget()
        self.topic_list_scroll_area_content.setGeometry(QtCore.QRect(0, 0, 714, 312))
        self.topic_list_scroll_area_content.setObjectName("topic_list_scroll_area_content")

        self.topic_list_vertical_layout = QtWidgets.QVBoxLayout(self.topic_list_scroll_area_content)
        self.topic_list_vertical_layout.setContentsMargins(0, 10, 0, 0)
        self.topic_list_vertical_layout.setSpacing(5)
        self.topic_list_vertical_layout.setObjectName("topic_list_vertical_layout")
        
        self.subject_group_box = QtWidgets.QGroupBox(parent=self.topic_list_scroll_area_content)
        self.subject_group_box.setTitle("")
        self.subject_group_box.setObjectName("subject_group_box")

        self.subject_horizontal_layout = QtWidgets.QHBoxLayout(self.subject_group_box)
        self.subject_horizontal_layout.setContentsMargins(0, 0, 0, 0)
        self.subject_horizontal_layout.setSpacing(5)
        self.subject_horizontal_layout.setObjectName("subject_horizontal_layout")

        spacerItem3 = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Policy.Expanding, QtWidgets.QSizePolicy.Policy.Minimum)
        self.subject_horizontal_layout.addItem(spacerItem3)

        self.course_subject_label = QtWidgets.QLabel(parent=self.subject_group_box)
        font = QtGui.QFont()
        font.setPointSize(self.static["font-sizes"]["text"])
        self.course_subject_label.setMinimumHeight(self.static["topic"]["height"]-10)
        self.course_subject_label.setFont(font)
        self.course_subject_label.setStyleSheet("background-color: #D9F2D0; border: 2px solid white; border-radius:10; padding-left:20px;padding-right:20px")
        self.course_subject_label.setObjectName("course_subject_label")
        self.subject_horizontal_layout.addWidget(self.course_subject_label)

        self.subject_combo_box = QtWidgets.QComboBox(parent=self.subject_group_box)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Policy.Maximum, QtWidgets.QSizePolicy.Policy.Fixed)
        self.subject_combo_box.setSizePolicy(sizePolicy)
        self.subject_combo_box.setMinimumSize(QtCore.QSize(self.static["topic"]["small-width"], self.static["topic"]["height"]-10))
        font = QtGui.QFont()
        font.setPointSize(self.static["font-sizes"]["text"])
        self.subject_combo_box.setFont(font)
        self.subject_combo_box.setCursor(QtGui.QCursor(QtCore.Qt.CursorShape.PointingHandCursor))
        self.subject_combo_box.setStyleSheet("QComboBox {background-color: #D9F2D0; border: 2px solid black; border-radius:10; padding-left:20px;padding-right:20px;}\n"
                                            "QComboBox:hover {background-color: #55aa00; border: 2px solid black; border-radius:10; padding-left:20px;padding-right:20px;}\n"
                                            "QAbstractItemView{selection-color: black; selection-background-color: #55aa00; background-color: #D9F2D0; border: 2px solid black; border-radius:10; padding-left:20px;padding-right:20px;padding-top:5px; padding-bottom:5px;}")
        self.subject_combo_box.setObjectName("subject_combo_box")
        self.subject_combo_box.addItem("")
        self.subject_combo_box.setItemText(0, "")
        self.subject_horizontal_layout.addWidget(self.subject_combo_box)        

        spacerItem4 = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Policy.Expanding, QtWidgets.QSizePolicy.Policy.Minimum)
        self.subject_horizontal_layout.addItem(spacerItem4)
        self.topic_list_vertical_layout.addWidget(self.subject_group_box)        

        self.topic_list_group_box = QtWidgets.QGroupBox(parent=self.topic_list_scroll_area_content)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Policy.Expanding, QtWidgets.QSizePolicy.Policy.Expanding)
        #sizePolicy.setHeightForWidth(self.topic_list_group_box.sizePolicy().hasHeightForWidth())
        self.topic_list_group_box.setSizePolicy(sizePolicy)
        self.topic_list_group_box.setTitle("")
        self.topic_list_group_box.setObjectName("topic_list_group_box")

        self.topic_list_horizontal_layout = QtWidgets.QHBoxLayout(self.topic_list_group_box)
        self.topic_list_horizontal_layout.setContentsMargins(0, 10, 0, 0)
        self.topic_list_horizontal_layout.setSpacing(5)
        self.topic_list_horizontal_layout.setObjectName("topic_list_horizontal_layout")

        self.topic_list_vertical_layout.addWidget(self.topic_list_group_box)

        self.topic_list_scroll_area.setWidget(self.topic_list_scroll_area_content)
        self.topic_tab_vertical_layout.addWidget(self.topic_list_scroll_area)
        self.tabWidget.addTab(self.topic_tab, "")
        self.teacher_main_page_vertical_layout.addWidget(self.tabWidget)

        self.retranslateUi(teacher_main_page)

        match teacher_main_page.user_settings['font-size']:
            case 'small':
                self.font_size_combo_box.setCurrentIndex(0)
            case 'medium':
                self.font_size_combo_box.setCurrentIndex(1)
            case 'big':
                self.font_size_combo_box.setCurrentIndex(2)
        self.tabWidget.setCurrentIndex(0)
        QtCore.QMetaObject.connectSlotsByName(teacher_main_page)

    def retranslateUi(self, teacher_main_page):
        _translate = QtCore.QCoreApplication.translate
        teacher_main_page.setWindowTitle(_translate("teacher_main_page", "SmartStudy"))
        teacher_main_page.setWindowIcon(QtGui.QIcon("utils/images/window-icon.png"))
        self.menu_label.setText(_translate("teacher_main_page", "Oktatói kezdőlap"))
        self.font_size_combo_box.setItemText(0, _translate("teacher_main_page", "Kis betűméret"))
        self.font_size_combo_box.setItemText(1, _translate("teacher_main_page", "Közepes betűméret"))
        self.font_size_combo_box.setItemText(2, _translate("teacher_main_page", "Nagy betűméret"))
        self.logout_cmd_link_btn.setText(_translate("teacher_main_page", "Kijelentkezés"))
        self.teacher_name_label.setText(_translate("teacher_main_page", teacher_main_page.name))        
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.class_tab), _translate("teacher_main_page", "Osztályok"))
        self.course_subject_label.setText(_translate("teacher_main_page", "Tantárgy:"))
        """topic_title_btn.setText(_translate("teacher_main_page", "topic_title_1"))
        topic_desc_label.setText(_translate("teacher_main_page", "topic_desc_1"))"""
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.topic_tab), _translate("teacher_main_page", "Témakörök"))
