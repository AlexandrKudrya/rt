# -*- coding: utf-8 -*-
import sys
from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtWidgets import QApplication
from question import ques


class QQButton(QtWidgets.QPushButton):
    def __init__(self):
        super(QQButton, self).__init__()
        self.value = ['1', '1', '1']
        self.clicked.connect(self.ques)
        self.setText("Вопрос не установлен")

    def ques(self):
        ques(self, self.value)
        self.setText("Вопрос установлен")


class Test_Creator(QtWidgets.QWidget):
    def __init__(self):
        super(Test_Creator, self).__init__()
        self.last_ques = 0
        self.setupUi(self)
        self.arr_questions = []

    def setupUi(self, Form):
        Form.setObjectName("Form")
        Form.resize(875, 771)
        self.title_test = QtWidgets.QLineEdit(Form)
        self.title_test.setGeometry(QtCore.QRect(10, 30, 351, 20))
        self.title_test.setObjectName("title_test")
        self.count_of_questions = QtWidgets.QSpinBox(Form)
        self.count_of_questions.setGeometry(QtCore.QRect(260, 60, 101, 22))
        self.count_of_questions.setObjectName("count_of_questions")
        self.verticalLayoutWidget = QtWidgets.QWidget(Form)
        self.verticalLayoutWidget.setGeometry(QtCore.QRect(20, 89, 341, 671))
        self.verticalLayoutWidget.setObjectName("verticalLayoutWidget")
        self.questions = QtWidgets.QVBoxLayout(self.verticalLayoutWidget)
        self.questions.setContentsMargins(0, 0, 0, 0)
        self.questions.setObjectName("questions")
        self.label = QtWidgets.QLabel(Form)
        self.label.setGeometry(QtCore.QRect(10, 10, 61, 16))
        self.label.setObjectName("label")
        self.label_2 = QtWidgets.QLabel(Form)
        self.label_2.setGeometry(QtCore.QRect(156, 60, 91, 20))
        self.label_2.setObjectName("label_2")
        self.classes = QtWidgets.QComboBox(Form)
        self.classes.setGeometry(QtCore.QRect(410, 30, 441, 22))
        self.classes.setObjectName("classes")
        self.label_3 = QtWidgets.QLabel(Form)
        self.label_3.setGeometry(QtCore.QRect(410, 3, 47, 20))
        self.label_3.setObjectName("label_3")
        self.email = QtWidgets.QLineEdit(Form)
        self.email.setGeometry(QtCore.QRect(410, 80, 441, 22))
        self.email.setObjectName("email")
        self.label_4 = QtWidgets.QLabel(Form)
        self.label_4.setGeometry(QtCore.QRect(410, 60, 441, 22))
        self.label_4.setObjectName("label_4")
        self.save_test = QtWidgets.QPushButton(Form)
        self.save_test.setGeometry(QtCore.QRect(780, 730, 75, 31))
        self.save_test.setObjectName("save_test")

        self.retranslateUi(Form)
        QtCore.QMetaObject.connectSlotsByName(Form)

    def retranslateUi(self, Form):
        _translate = QtCore.QCoreApplication.translate
        Form.setWindowTitle(_translate("Form", "Form"))
        self.label.setText(_translate("Form", "Название"))
        self.label_2.setText(_translate("Form", "Кол-во вопросов"))
        self.label_3.setText(_translate("Form", "Классы"))
        self.label_4.setText(_translate("FOrm", "Почта получателя результатов"))
        self.save_test.setText(_translate("Form", "Сохранить"))

        self.count_of_questions.valueChanged.connect(self.requestion)
        self.save_test.clicked.connect(self.save)
        self.classes.addItems([str(i) for i in range(1, 12)])

    def requestion(self):
        if self.count_of_questions.value() <= self.last_ques:
            for i in range(self.last_ques - self.count_of_questions.value()):
                self.arr_questions[-1].deleteLater()
                del self.arr_questions[-1]
        else:
            for i in range(abs(self.last_ques - self.count_of_questions.value())):
                k = QQButton()
                k.setParent(self)
                self.questions.addWidget(k)
                self.arr_questions.append(k)
        self.last_ques = self.count_of_questions.value()

    def save(self):
        arr = [self.title_test.text().replace(" ", "_"), self.classes.currentText()]
        file = open(f"tests/{'_'.join(arr)}", encoding="utf-8", mode="w")
        file.write(self.email.text() + '\n')
        for i in self.arr_questions:
            file.write('(' + ','.join(i.value) + ')\n')
        file.close()

if __name__ == "__main__":
    app = QApplication(sys.argv)
    ex = Test_Creator()
    ex.show()
    sys.exit(app.exec())