# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'analyzing.ui'
#
# Created by: PyQt5 UI code generator 5.15.4
#
# WARNING: Any manual changes made to this file will be lost when pyuic5 is
# run again.


from PyQt5 import QtCore, QtGui, QtWidgets


class Ui_AnalyzingPage(QtCore.QObject):
    def setupUi(self, AnalyzingPage):
        self.AnalyzingPage = AnalyzingPage
        AnalyzingPage.setObjectName("AnalyzingPage")
        AnalyzingPage.resize(730, 612)
        AnalyzingPage.setStyleSheet("color: #1d1e1f;")
        self.verticalLayout = QtWidgets.QVBoxLayout(AnalyzingPage)
        self.verticalLayout.setSpacing(15)
        self.verticalLayout.setObjectName("verticalLayout")
        self.EvaluatingCriteria = QtWidgets.QLabel(AnalyzingPage)
        sizePolicy = QtWidgets.QSizePolicy(
            QtWidgets.QSizePolicy.Preferred, QtWidgets.QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(
            self.EvaluatingCriteria.sizePolicy().hasHeightForWidth())
        self.EvaluatingCriteria.setSizePolicy(sizePolicy)
        font = QtGui.QFont()
        font.setPointSize(12)
        self.EvaluatingCriteria.setFont(font)
        self.EvaluatingCriteria.setAlignment(
            QtCore.Qt.AlignLeading | QtCore.Qt.AlignLeft | QtCore.Qt.AlignVCenter)
        self.EvaluatingCriteria.setObjectName("EvaluatingCriteria")
        self.verticalLayout.addWidget(
            self.EvaluatingCriteria, 0, QtCore.Qt.AlignHCenter | QtCore.Qt.AlignBottom)
        self.Image = QtWidgets.QLabel(AnalyzingPage)
        sizePolicy = QtWidgets.QSizePolicy(
            QtWidgets.QSizePolicy.Preferred, QtWidgets.QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(
            self.Image.sizePolicy().hasHeightForWidth())
        self.Image.setSizePolicy(sizePolicy)
        self.Image.setText("")
        self.Image.setObjectName("Image")
        self.verticalLayout.addWidget(
            self.Image, 0, QtCore.Qt.AlignHCenter | QtCore.Qt.AlignVCenter)
        self.spacer = QtWidgets.QLabel(AnalyzingPage)
        sizePolicy = QtWidgets.QSizePolicy(
            QtWidgets.QSizePolicy.Preferred, QtWidgets.QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(
            self.spacer.sizePolicy().hasHeightForWidth())
        self.spacer.setSizePolicy(sizePolicy)
        self.spacer.setText("")
        self.spacer.setObjectName("spacer")
        self.verticalLayout.addWidget(self.spacer)

        self.retranslateUi(AnalyzingPage)
        QtCore.QMetaObject.connectSlotsByName(AnalyzingPage)

        self.imagePath = ""

        AnalyzingPage.installEventFilter(self)

    def retranslateUi(self, AnalyzingPage):
        _translate = QtCore.QCoreApplication.translate
        AnalyzingPage.setWindowTitle(_translate("AnalyzingPage", "Form"))
        self.EvaluatingCriteria.setText(_translate(
            "AnalyzingPage", "Evaluating <criteria>"))

    def setCriteria(self, criteria):
        self.EvaluatingCriteria.setText("Analyzing %s ..." % criteria)

    def setImage(self, path):
        self.imagePath = path
        height = self.AnalyzingPage.height() / 1.5
        self.Image.setPixmap(QtGui.QPixmap(path).scaled(
            height, height, QtCore.Qt.KeepAspectRatio))

    def eventFilter(self, obj, event):
        if (event.type() == QtCore.QEvent.Resize and self.imagePath != ""):
            self.setImage(self.imagePath)
        return super().eventFilter(obj, event)


if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    AnalyzingPage = QtWidgets.QWidget()
    ui = Ui_AnalyzingPage()
    ui.setupUi(AnalyzingPage)
    AnalyzingPage.show()
    sys.exit(app.exec_())
