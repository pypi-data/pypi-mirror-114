# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'settings.ui'
#
# Created by: PyQt5 UI code generator 5.15.4
#
# WARNING: Any manual changes made to this file will be lost when pyuic5 is
# run again.


from PyQt5 import QtCore, QtGui, QtWidgets


class Ui_Settings(QtCore.QObject):
    criteriaChangedSignal = QtCore.pyqtSignal(str, int)
    thresholdChangedSignal = QtCore.pyqtSignal(float)

    def setupUi(self, Settings):
        Settings.setObjectName("Settings")
        Settings.resize(898, 603)
        sizePolicy = QtWidgets.QSizePolicy(
            QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(Settings.sizePolicy().hasHeightForWidth())
        Settings.setSizePolicy(sizePolicy)
        Settings.setStyleSheet("QFrame {\n"
                               "color:  #00ffff;\n"
                               "}\n"
                               "QLabel, QPushButton {\n"
                               "color: #1d1e1f;\n"
                               "}\n"
                               "\n"
                               "")
        self.verticalLayout = QtWidgets.QVBoxLayout(Settings)
        self.verticalLayout.setObjectName("verticalLayout")
        self.Back = QtWidgets.QPushButton(Settings)
        self.Back.setCursor(
            QtGui.QCursor(QtCore.Qt.PointingHandCursor))
        sizePolicy = QtWidgets.QSizePolicy(
            QtWidgets.QSizePolicy.Preferred, QtWidgets.QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(
            self.Back.sizePolicy().hasHeightForWidth())
        self.Back.setSizePolicy(sizePolicy)
        font = QtGui.QFont()
        font.setPointSize(14)
        font.setBold(True)
        font.setWeight(75)
        self.Back.setFont(font)
        self.Back.setStyleSheet("border: bold")
        icon = QtGui.QIcon()
        icon.addPixmap(QtGui.QPixmap(":/img/back-button.png"),
                       QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.Back.setIcon(icon)
        self.Back.setIconSize(QtCore.QSize(50, 50))
        self.Back.setObjectName("Back")
        self.verticalLayout.addWidget(
            self.Back, 0, QtCore.Qt.AlignLeft | QtCore.Qt.AlignTop)
        spacerItem = QtWidgets.QSpacerItem(
            20, 40, QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Expanding)
        self.verticalLayout.addItem(spacerItem)
        self.frame = QtWidgets.QFrame(Settings)
        self.frame.setStyleSheet("QRadioButton::indicator {\n"
                                 "    width:10px;\n"
                                 "    height:10px;\n"
                                 "    border-radius: 8px;\n"
                                 "    border: 3px solid #57AECB;\n"
                                 "}\n"
                                 "\n"
                                 "QRadioButton::indicator:unchecked  {\n"
                                 "    background: transparent;\n"
                                 "}\n"
                                 "\n"
                                 "QRadioButton::indicator:checked  {\n"
                                 "    background: #87CEEB;\n"
                                 "}")
        sizePolicy = QtWidgets.QSizePolicy(
            QtWidgets.QSizePolicy.Preferred, QtWidgets.QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(
            self.frame.sizePolicy().hasHeightForWidth())
        self.frame.setSizePolicy(sizePolicy)
        self.frame.setMinimumSize(QtCore.QSize(880, 290))
        self.frame.setFrameShape(QtWidgets.QFrame.StyledPanel)
        self.frame.setFrameShadow(QtWidgets.QFrame.Raised)
        self.frame.setObjectName("frame")
        self.horizontalSlider = QtWidgets.QSlider(self.frame)
        self.horizontalSlider.setGeometry(QtCore.QRect(220, 15, 641, 22))
        self.horizontalSlider.setStyleSheet("QSlider::groove:horizontal {\n"
                                            "    border: 1px solid #999999;\n"
                                            "    height: 4px;\n"
                                            "    margin:0px 0;\n"
                                            "}\n"
                                            "\n"
                                            "QSlider::handle:horizontal {\n"
                                            "    background: #87CEEB;\n"
                                            "    border: 3px solid #57AECB;\n"
                                            "    width: 10px;\n"
                                            "    margin: -6px 0; \n"
                                            "    border-radius: 8px;\n"
                                            "}\n"
                                            "\n"
                                            "QSlider::sub-page:horizontal {\n"
                                            "    height: 1px;\n"
                                            "    background:  #87CEEB;\n"
                                            "}")
        self.horizontalSlider.setMinimum(70)
        self.horizontalSlider.setMaximum(95)
        self.horizontalSlider.setProperty("value", 80)
        self.horizontalSlider.setOrientation(QtCore.Qt.Horizontal)
        self.horizontalSlider.setObjectName("horizontalSlider")
        self.Threshhold = QtWidgets.QLabel(self.frame)
        self.Threshhold.setGeometry(QtCore.QRect(10, 10, 187, 25))
        font = QtGui.QFont()
        font.setPointSize(12)
        self.Threshhold.setFont(font)
        self.Threshhold.setAlignment(
            QtCore.Qt.AlignLeading | QtCore.Qt.AlignLeft | QtCore.Qt.AlignVCenter)
        self.Threshhold.setObjectName("Threshhold")
        self.Important = QtWidgets.QLabel(self.frame)
        self.Important.setGeometry(QtCore.QRect(572, 50, 94, 113))
        sizePolicy = QtWidgets.QSizePolicy(
            QtWidgets.QSizePolicy.Preferred, QtWidgets.QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(1)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(
            self.Important.sizePolicy().hasHeightForWidth())
        self.Important.setSizePolicy(sizePolicy)
        font = QtGui.QFont()
        font.setFamily("MS Shell Dlg 2")
        font.setPointSize(12)
        self.Important.setFont(font)
        self.Important.setAlignment(
            QtCore.Qt.AlignLeading | QtCore.Qt.AlignLeft | QtCore.Qt.AlignVCenter)
        self.Important.setObjectName("Important")
        self.SomewhatImp = QtWidgets.QLabel(self.frame)
        self.SomewhatImp.setGeometry(QtCore.QRect(372, 50, 149, 113))
        sizePolicy = QtWidgets.QSizePolicy(
            QtWidgets.QSizePolicy.Preferred, QtWidgets.QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(1)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(
            self.SomewhatImp.sizePolicy().hasHeightForWidth())
        self.SomewhatImp.setSizePolicy(sizePolicy)
        font = QtGui.QFont()
        font.setFamily("MS Shell Dlg 2")
        font.setPointSize(12)
        self.SomewhatImp.setFont(font)
        self.SomewhatImp.setAlignment(
            QtCore.Qt.AlignLeading | QtCore.Qt.AlignLeft | QtCore.Qt.AlignVCenter)
        self.SomewhatImp.setObjectName("SomewhatImp")
        self.VeryImportant = QtWidgets.QLabel(self.frame)
        self.VeryImportant.setGeometry(QtCore.QRect(720, 50, 143, 113))
        sizePolicy = QtWidgets.QSizePolicy(
            QtWidgets.QSizePolicy.Preferred, QtWidgets.QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(1)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(
            self.VeryImportant.sizePolicy().hasHeightForWidth())
        self.VeryImportant.setSizePolicy(sizePolicy)
        font = QtGui.QFont()
        font.setFamily("MS Shell Dlg 2")
        font.setPointSize(12)
        self.VeryImportant.setFont(font)
        self.VeryImportant.setAlignment(
            QtCore.Qt.AlignLeading | QtCore.Qt.AlignLeft | QtCore.Qt.AlignVCenter)
        self.VeryImportant.setObjectName("VeryImportant")
        self.DoNotConsider = QtWidgets.QLabel(self.frame)
        self.DoNotConsider.setGeometry(QtCore.QRect(190, 50, 147, 113))
        sizePolicy = QtWidgets.QSizePolicy(
            QtWidgets.QSizePolicy.Preferred, QtWidgets.QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(1)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(
            self.DoNotConsider.sizePolicy().hasHeightForWidth())
        self.DoNotConsider.setSizePolicy(sizePolicy)
        font = QtGui.QFont()
        font.setFamily("MS Shell Dlg 2")
        font.setPointSize(12)
        self.DoNotConsider.setFont(font)
        self.DoNotConsider.setAlignment(
            QtCore.Qt.AlignLeading | QtCore.Qt.AlignLeft | QtCore.Qt.AlignVCenter)
        self.DoNotConsider.setObjectName("DoNotConsider")
        self.Sharpness = QtWidgets.QLabel(self.frame)
        self.Sharpness.setGeometry(QtCore.QRect(30, 135, 147, 31))
        sizePolicy = QtWidgets.QSizePolicy(
            QtWidgets.QSizePolicy.Preferred, QtWidgets.QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(1)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(
            self.Sharpness.sizePolicy().hasHeightForWidth())
        self.Sharpness.setSizePolicy(sizePolicy)
        font = QtGui.QFont()
        font.setFamily("MS Shell Dlg 2")
        font.setPointSize(12)
        self.Sharpness.setFont(font)
        self.Sharpness.setAlignment(
            QtCore.Qt.AlignLeading | QtCore.Qt.AlignLeft | QtCore.Qt.AlignVCenter)
        self.Sharpness.setObjectName("Sharpness")
        self.Centering = QtWidgets.QLabel(self.frame)
        self.Centering.setGeometry(QtCore.QRect(30, 175, 147, 31))
        sizePolicy = QtWidgets.QSizePolicy(
            QtWidgets.QSizePolicy.Preferred, QtWidgets.QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(1)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(
            self.Centering.sizePolicy().hasHeightForWidth())
        self.Centering.setSizePolicy(sizePolicy)
        font = QtGui.QFont()
        font.setFamily("MS Shell Dlg 2")
        font.setPointSize(12)
        self.Centering.setFont(font)
        self.Centering.setAlignment(
            QtCore.Qt.AlignLeading | QtCore.Qt.AlignLeft | QtCore.Qt.AlignVCenter)
        self.Centering.setObjectName("Centering")
        self.Lighting = QtWidgets.QLabel(self.frame)
        self.Lighting.setGeometry(QtCore.QRect(30, 215, 147, 31))
        sizePolicy = QtWidgets.QSizePolicy(
            QtWidgets.QSizePolicy.Preferred, QtWidgets.QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(1)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(
            self.Lighting.sizePolicy().hasHeightForWidth())
        self.Lighting.setSizePolicy(sizePolicy)
        font = QtGui.QFont()
        font.setFamily("MS Shell Dlg 2")
        font.setPointSize(12)
        self.Lighting.setFont(font)
        self.Lighting.setAlignment(
            QtCore.Qt.AlignLeading | QtCore.Qt.AlignLeft | QtCore.Qt.AlignVCenter)
        self.Lighting.setObjectName("Lighting")
        self.Resolution = QtWidgets.QLabel(self.frame)
        self.Resolution.setGeometry(QtCore.QRect(30, 255, 147, 31))
        sizePolicy = QtWidgets.QSizePolicy(
            QtWidgets.QSizePolicy.Preferred, QtWidgets.QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(1)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(
            self.Resolution.sizePolicy().hasHeightForWidth())
        self.Resolution.setSizePolicy(sizePolicy)
        font = QtGui.QFont()
        font.setFamily("MS Shell Dlg 2")
        font.setPointSize(12)
        self.Resolution.setFont(font)
        self.Resolution.setAlignment(
            QtCore.Qt.AlignLeading | QtCore.Qt.AlignLeft | QtCore.Qt.AlignVCenter)
        self.Resolution.setObjectName("Resolution")
        self.line = QtWidgets.QFrame(self.frame)
        self.line.setGeometry(QtCore.QRect(0, 120, 881, 20))
        self.line.setFrameShadow(QtWidgets.QFrame.Plain)
        self.line.setLineWidth(1)
        self.line.setFrameShape(QtWidgets.QFrame.HLine)
        self.line.setObjectName("line")
        self.line_2 = QtWidgets.QFrame(self.frame)
        self.line_2.setGeometry(QtCore.QRect(0, 160, 881, 20))
        self.line_2.setFrameShadow(QtWidgets.QFrame.Plain)
        self.line_2.setLineWidth(1)
        self.line_2.setFrameShape(QtWidgets.QFrame.HLine)
        self.line_2.setObjectName("line_2")
        self.line_3 = QtWidgets.QFrame(self.frame)
        self.line_3.setGeometry(QtCore.QRect(0, 200, 881, 20))
        self.line_3.setFrameShadow(QtWidgets.QFrame.Plain)
        self.line_3.setLineWidth(1)
        self.line_3.setFrameShape(QtWidgets.QFrame.HLine)
        self.line_3.setObjectName("line_3")
        self.line_4 = QtWidgets.QFrame(self.frame)
        self.line_4.setGeometry(QtCore.QRect(0, 240, 881, 20))
        self.line_4.setFrameShadow(QtWidgets.QFrame.Plain)
        self.line_4.setLineWidth(1)
        self.line_4.setFrameShape(QtWidgets.QFrame.HLine)
        self.line_4.setObjectName("line_4")
        self.line_5 = QtWidgets.QFrame(self.frame)
        self.line_5.setGeometry(QtCore.QRect(160, 90, 20, 201))
        self.line_5.setStyleSheet("")
        self.line_5.setFrameShadow(QtWidgets.QFrame.Plain)
        self.line_5.setLineWidth(1)
        self.line_5.setFrameShape(QtWidgets.QFrame.VLine)
        self.line_5.setObjectName("line_5")
        self.line_6 = QtWidgets.QFrame(self.frame)
        self.line_6.setGeometry(QtCore.QRect(350, 90, 20, 201))
        self.line_6.setFrameShadow(QtWidgets.QFrame.Plain)
        self.line_6.setLineWidth(1)
        self.line_6.setFrameShape(QtWidgets.QFrame.VLine)
        self.line_6.setObjectName("line_6")
        self.line_7 = QtWidgets.QFrame(self.frame)
        self.line_7.setGeometry(QtCore.QRect(540, 90, 20, 201))
        self.line_7.setFrameShadow(QtWidgets.QFrame.Plain)
        self.line_7.setLineWidth(1)
        self.line_7.setFrameShape(QtWidgets.QFrame.VLine)
        self.line_7.setObjectName("line_7")
        self.line_8 = QtWidgets.QFrame(self.frame)
        self.line_8.setGeometry(QtCore.QRect(690, 90, 20, 201))
        self.line_8.setFrameShadow(QtWidgets.QFrame.Plain)
        self.line_8.setLineWidth(1)
        self.line_8.setFrameShape(QtWidgets.QFrame.VLine)
        self.line_8.setObjectName("line_8")
        self.frame_6 = QtWidgets.QFrame(self.frame)
        self.frame_6.setGeometry(QtCore.QRect(0, 90, 880, 200))
        self.frame_6.setStyleSheet("QFrame {\n"
                                   "    border: 1px solid #b187eb;\n"
                                   "}")
        self.frame_6.setFrameShape(QtWidgets.QFrame.StyledPanel)
        self.frame_6.setFrameShadow(QtWidgets.QFrame.Raised)
        self.frame_6.setObjectName("frame_6")

        self.SharpnessButtons = QtWidgets.QFrame(self.frame)
        self.SharpnessButtons.setGeometry(QtCore.QRect(253, 143, 540, 20))
        self.SharpnessButtons.setFrameShape(QtWidgets.QFrame.StyledPanel)
        self.SharpnessButtons.setFrameShadow(QtWidgets.QFrame.Raised)
        self.SharpnessButtons.setObjectName("SharpnessButtons")
        self.sharpness_3 = QtWidgets.QRadioButton(self.SharpnessButtons)
        self.sharpness_3.setGeometry(QtCore.QRect(520, 0, 16, 17))
        self.sharpness_3.setText("")
        self.sharpness_3.setChecked(False)
        self.sharpness_3.setObjectName("sharpness_3")
        self.sharpness_0 = QtWidgets.QRadioButton(self.SharpnessButtons)
        self.sharpness_0.setGeometry(QtCore.QRect(0, 0, 16, 17))
        self.sharpness_0.setText("")
        self.sharpness_0.setChecked(True)
        self.sharpness_0.setObjectName("sharpness_0")
        self.sharpness_1 = QtWidgets.QRadioButton(self.SharpnessButtons)
        self.sharpness_1.setGeometry(QtCore.QRect(190, 0, 16, 17))
        self.sharpness_1.setText("")
        self.sharpness_1.setChecked(False)
        self.sharpness_1.setObjectName("sharpness_1")
        self.sharpness_2 = QtWidgets.QRadioButton(self.SharpnessButtons)
        self.sharpness_2.setGeometry(QtCore.QRect(360, 0, 16, 17))
        self.sharpness_2.setText("")
        self.sharpness_2.setChecked(False)
        self.sharpness_2.setObjectName("sharpness_2")
        self.CenteringButtons = QtWidgets.QFrame(self.frame)
        self.CenteringButtons.setGeometry(QtCore.QRect(253, 183, 540, 20))
        self.CenteringButtons.setFrameShape(QtWidgets.QFrame.StyledPanel)
        self.CenteringButtons.setFrameShadow(QtWidgets.QFrame.Raised)
        self.CenteringButtons.setObjectName("CenteringButtons")
        self.centering_3 = QtWidgets.QRadioButton(self.CenteringButtons)
        self.centering_3.setGeometry(QtCore.QRect(520, 0, 16, 17))
        self.centering_3.setText("")
        self.centering_3.setChecked(False)
        self.centering_3.setObjectName("centering_3")
        self.centering_0 = QtWidgets.QRadioButton(self.CenteringButtons)
        self.centering_0.setGeometry(QtCore.QRect(0, 0, 16, 17))
        self.centering_0.setText("")
        self.centering_0.setChecked(True)
        self.centering_0.setObjectName("centering_0")
        self.centering_1 = QtWidgets.QRadioButton(self.CenteringButtons)
        self.centering_1.setGeometry(QtCore.QRect(190, 0, 16, 17))
        self.centering_1.setText("")
        self.centering_1.setChecked(False)
        self.centering_1.setObjectName("centering_1")
        self.centering_2 = QtWidgets.QRadioButton(self.CenteringButtons)
        self.centering_2.setGeometry(QtCore.QRect(360, 0, 16, 17))
        self.centering_2.setText("")
        self.centering_2.setChecked(False)
        self.centering_2.setObjectName("centering_2")
        self.LightingButtons = QtWidgets.QFrame(self.frame)
        self.LightingButtons.setGeometry(QtCore.QRect(253, 223, 540, 20))
        self.LightingButtons.setFrameShape(QtWidgets.QFrame.StyledPanel)
        self.LightingButtons.setFrameShadow(QtWidgets.QFrame.Raised)
        self.LightingButtons.setObjectName("LightingButtons")
        self.lighting_3 = QtWidgets.QRadioButton(self.LightingButtons)
        self.lighting_3.setGeometry(QtCore.QRect(520, 0, 16, 17))
        self.lighting_3.setText("")
        self.lighting_3.setChecked(False)
        self.lighting_3.setObjectName("lighting_3")
        self.lighting_0 = QtWidgets.QRadioButton(self.LightingButtons)
        self.lighting_0.setGeometry(QtCore.QRect(0, 0, 16, 17))
        self.lighting_0.setText("")
        self.lighting_0.setChecked(True)
        self.lighting_0.setObjectName("lighting_0")
        self.lighting_1 = QtWidgets.QRadioButton(self.LightingButtons)
        self.lighting_1.setGeometry(QtCore.QRect(190, 0, 16, 17))
        self.lighting_1.setText("")
        self.lighting_1.setChecked(False)
        self.lighting_1.setObjectName("lighting_1")
        self.lighting_2 = QtWidgets.QRadioButton(self.LightingButtons)
        self.lighting_2.setGeometry(QtCore.QRect(360, 0, 16, 17))
        self.lighting_2.setText("")
        self.lighting_2.setChecked(False)
        self.lighting_2.setObjectName("lighting_2")
        self.ResolutionButtons = QtWidgets.QFrame(self.frame)
        self.ResolutionButtons.setGeometry(QtCore.QRect(253, 263, 540, 20))
        self.ResolutionButtons.setFrameShape(QtWidgets.QFrame.StyledPanel)
        self.ResolutionButtons.setFrameShadow(QtWidgets.QFrame.Raised)
        self.ResolutionButtons.setObjectName("ResolutionButtons")
        self.resolution_3 = QtWidgets.QRadioButton(self.ResolutionButtons)
        self.resolution_3.setGeometry(QtCore.QRect(520, 0, 16, 17))
        self.resolution_3.setText("")
        self.resolution_3.setChecked(False)
        self.resolution_3.setObjectName("resolution_3")
        self.resolution_0 = QtWidgets.QRadioButton(self.ResolutionButtons)
        self.resolution_0.setGeometry(QtCore.QRect(0, 0, 16, 17))
        self.resolution_0.setText("")
        self.resolution_0.setChecked(True)
        self.resolution_0.setObjectName("resolution_0")
        self.resolution_1 = QtWidgets.QRadioButton(self.ResolutionButtons)
        self.resolution_1.setGeometry(QtCore.QRect(190, 0, 16, 17))
        self.resolution_1.setText("")
        self.resolution_1.setChecked(False)
        self.resolution_1.setObjectName("resolution_1")
        self.resolution_2 = QtWidgets.QRadioButton(self.ResolutionButtons)
        self.resolution_2.setGeometry(QtCore.QRect(360, 0, 16, 17))
        self.resolution_2.setText("")
        self.resolution_2.setChecked(False)
        self.resolution_2.setObjectName("resolution_2")
        self.verticalLayout.addWidget(self.frame, 0, QtCore.Qt.AlignHCenter)
        spacerItem1 = QtWidgets.QSpacerItem(
            20, 40, QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Expanding)
        self.verticalLayout.addItem(spacerItem1)

        self.retranslateUi(Settings)
        QtCore.QMetaObject.connectSlotsByName(Settings)

        self.sharpnessButtonGroup = QtWidgets.QButtonGroup()
        self.sharpnessButtonGroup.addButton(self.sharpness_0, 0)
        self.sharpnessButtonGroup.addButton(self.sharpness_1, 1)
        self.sharpnessButtonGroup.addButton(self.sharpness_2, 2)
        self.sharpnessButtonGroup.addButton(self.sharpness_3, 3)
        self.sharpnessButtonGroup.buttonClicked.connect(
            self.onSharpnessChanged)

        self.centeringButtonGroup = QtWidgets.QButtonGroup()
        self.centeringButtonGroup.addButton(self.centering_0, 0)
        self.centeringButtonGroup.addButton(self.centering_1, 1)
        self.centeringButtonGroup.addButton(self.centering_2, 2)
        self.centeringButtonGroup.addButton(self.centering_3, 3)
        self.centeringButtonGroup.buttonClicked.connect(
            self.onCenteringChanged)

        self.lightingButtonGroup = QtWidgets.QButtonGroup()
        self.lightingButtonGroup.addButton(self.lighting_0, 0)
        self.lightingButtonGroup.addButton(self.lighting_1, 1)
        self.lightingButtonGroup.addButton(self.lighting_2, 2)
        self.lightingButtonGroup.addButton(self.lighting_3, 3)
        self.lightingButtonGroup.buttonClicked.connect(
            self.onLightingChanged)

        self.resolutionButtonGroup = QtWidgets.QButtonGroup()
        self.resolutionButtonGroup.addButton(self.resolution_0, 0)
        self.resolutionButtonGroup.addButton(self.resolution_1, 1)
        self.resolutionButtonGroup.addButton(self.resolution_2, 2)
        self.resolutionButtonGroup.addButton(self.resolution_3, 3)
        self.resolutionButtonGroup.buttonClicked.connect(
            self.onResolutionChanged)

        self.horizontalSlider.valueChanged.connect(self.onThresholdChanged)

    def retranslateUi(self, Settings):
        _translate = QtCore.QCoreApplication.translate
        Settings.setWindowTitle(_translate("Settings", "Form"))
        self.Back.setText(_translate("Settings", " Back"))
        self.Threshhold.setText(_translate(
            "Settings", "Similarity threshold:"))
        self.Important.setText(_translate("Settings", "Important"))
        self.SomewhatImp.setText(_translate("Settings", "Somewhat Imp."))
        self.VeryImportant.setText(_translate("Settings", "Very Important"))
        self.DoNotConsider.setText(_translate("Settings", "Do not consider"))
        self.Sharpness.setText(_translate("Settings", "Sharpness"))
        self.Centering.setText(_translate("Settings", "Centering"))
        self.Lighting.setText(_translate("Settings", "Lighting"))
        self.Resolution.setText(_translate("Settings", "Resolution"))

    def setSettings(self, settings):
        self.sharpnessButtonGroup.button(
            settings["sharpness"]).setChecked(True)
        self.centeringButtonGroup.button(
            settings["centering"]).setChecked(True)
        self.lightingButtonGroup.button(
            settings["lighting"]).setChecked(True)
        self.resolutionButtonGroup.button(
            settings["resolution"]).setChecked(True)
        self.horizontalSlider.setValue(int(settings["threshold"] * 100))

    def onSharpnessChanged(self, button):
        if button.isChecked():
            self.criteriaChangedSignal.emit(
                "sharpness", self.sharpnessButtonGroup.checkedId())

    def onCenteringChanged(self, button):
        if button.isChecked():
            self.criteriaChangedSignal.emit(
                "centering", self.centeringButtonGroup.checkedId())

    def onLightingChanged(self, button):
        if button.isChecked():
            self.criteriaChangedSignal.emit(
                "lighting", self.lightingButtonGroup.checkedId())

    def onResolutionChanged(self, button):
        if button.isChecked():
            self.criteriaChangedSignal.emit(
                "resolution", self.resolutionButtonGroup.checkedId())

    def onThresholdChanged(self, value):
        self.thresholdChangedSignal.emit(value / 100)


if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    Settings = QtWidgets.QWidget()
    ui = Ui_Settings()
    ui.setupUi(Settings)
    Settings.show()
    sys.exit(app.exec_())
