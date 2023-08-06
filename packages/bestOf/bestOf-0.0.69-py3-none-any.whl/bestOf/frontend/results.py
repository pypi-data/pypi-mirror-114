# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'results.ui'
#
# Created by: PyQt5 UI code generator 5.15.4
#
# WARNING: Any manual changes made to this file will be lost when pyuic5 is
# run again.


from PyQt5 import QtCore, QtGui, QtWidgets


def clearLayout(layout):
    if layout is not None:
        while layout.count():
            child = layout.takeAt(0)
            if child.widget() is not None:
                child.widget().deleteLater()
            elif child.layout() is not None:
                clearLayout(child.layout())


class SelectableImage(QtWidgets.QLabel):
    toggled = QtCore.pyqtSignal(bool, int)

    def __init__(self, id, parent=None):
        QtWidgets.QLabel.__init__(self, parent)
        self.selected = False
        self.id = id

    def mousePressEvent(self, event):
        self.selected = not self.selected
        if self.selected:
            self.setStyleSheet("border: 3px solid #87CEEB;")
        else:
            self.setStyleSheet("")
        self.toggled.emit(self.selected, self.id)


class Ui_Results(QtCore.QObject):
    imageToggledSignal = QtCore.pyqtSignal(bool, int)
    downloadSelectedSignal = QtCore.pyqtSignal()

    def setupUi(self, Form):
        Form.setObjectName("Form")
        Form.resize(696, 537)
        Form.setStyleSheet("color: #1d1e1f;")
        self.verticalLayout_2 = QtWidgets.QVBoxLayout(Form)
        self.verticalLayout_2.setObjectName("verticalLayout_2")
        self.Back = QtWidgets.QPushButton(Form)
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
        self.verticalLayout_2.addWidget(
            self.Back, 0, QtCore.Qt.AlignLeft | QtCore.Qt.AlignTop)
        self.scrollArea = QtWidgets.QScrollArea(Form)
        self.scrollArea.setStyleSheet(
            "background: transparent; border: none;")
        self.scrollArea.setWidgetResizable(True)
        self.scrollArea.setObjectName("scrollArea")
        self.scrollAreaWidgetContents = QtWidgets.QWidget()
        self.scrollAreaWidgetContents.setGeometry(QtCore.QRect(0, 0, 762, 444))
        self.scrollAreaWidgetContents.setObjectName("scrollAreaWidgetContents")
        self.verticalLayout = QtWidgets.QVBoxLayout(
            self.scrollAreaWidgetContents)
        self.verticalLayout.setSpacing(15)
        self.verticalLayout.setObjectName("verticalLayout")
        self.scrollArea.setWidget(self.scrollAreaWidgetContents)
        self.verticalLayout_2.addWidget(self.scrollArea)

        self.retranslateUi(Form)
        QtCore.QMetaObject.connectSlotsByName(Form)

    def retranslateUi(self, Form):
        _translate = QtCore.QCoreApplication.translate
        Form.setWindowTitle(_translate("Form", "Form"))
        self.Back.setText(_translate("Form", " Back"))

    def display(self, imageList, groups):
        clearLayout(self.verticalLayout)

        for pos, group in enumerate(groups):
            horizontalLayout = QtWidgets.QHBoxLayout()
            horizontalLayout.setSpacing(15)

            label = QtWidgets.QLabel()
            font = QtGui.QFont()
            font.setFamily("MS Shell Dlg 2")
            font.setPointSize(12)
            label.setFont(font)
            label.setText(str(pos + 1))

            horizontalLayout.addWidget(
                label, 0, QtCore.Qt.AlignHCenter | QtCore.Qt.AlignVCenter)

            for index in group:
                for item in imageList:
                    if item[0] == index:
                        image = SelectableImage(index)
                        image.setGeometry(0, 0, 200, 200)
                        sizePolicy = QtWidgets.QSizePolicy(
                            QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Fixed)
                        image.setSizePolicy(sizePolicy)
                        image.setPixmap(QtGui.QPixmap(item[1]).scaled(
                            200, 200, QtCore.Qt.KeepAspectRatio))
                        image.toggled.connect(
                            lambda s, i: self.imageToggledSignal.emit(s, i))
                        horizontalLayout.addWidget(image)

            spacer = QtWidgets.QSpacerItem(
                40, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
            horizontalLayout.addItem(spacer)
            self.verticalLayout.addLayout(horizontalLayout)

        spacer = QtWidgets.QSpacerItem(
            20, 40, QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Expanding)
        self.verticalLayout.addItem(spacer)

        font = QtGui.QFont()
        font.setPointSize(14)
        font.setBold(True)
        font.setWeight(75)
        Download = QtWidgets.QPushButton()
        icon = QtGui.QIcon()
        icon.addPixmap(QtGui.QPixmap(
            ":/img/download.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        Download.setIcon(icon)
        Download.setIconSize(QtCore.QSize(50, 50))
        Download.setFont(font)
        Download.setStyleSheet(
            "color: #87CEEB; background: transparent; border: none;")
        Download.setText("Download Selected")
        Download.clicked.connect(lambda: self.downloadSelectedSignal.emit())
        self.verticalLayout.addWidget(
            Download, 0, QtCore.Qt.AlignLeft | QtCore.Qt.AlignBottom)


if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    Form = QtWidgets.QWidget()
    ui = Ui_Results()
    ui.setupUi(Form)
    Form.show()
    sys.exit(app.exec_())

