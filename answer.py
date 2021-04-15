# -*- coding: utf-8 -*-
from PyQt5 import QtCore, QtGui, QtWidgets


class Answer_str(QtWidgets.QWidget):
    def __init__(self, answer, manswers):
        super(Answer_str, self).__init__()
        self.ans = answer
        self.setupUi(self)

    def setupUi(self, Form):
        Form.setObjectName("Form")
        Form.resize(411, 251)
        self.answer = QtWidgets.QLineEdit(Form)
        self.answer.setGeometry(QtCore.QRect(60, 20, 161, 21))
        self.answer.setObjectName("answer")
        self.label = QtWidgets.QLabel(Form)
        self.label.setGeometry(QtCore.QRect(10, 20, 47, 21))
        self.label.setObjectName("label")

        self.retranslateUi(Form)
        QtCore.QMetaObject.connectSlotsByName(Form)

    def retranslateUi(self, Form):
        _translate = QtCore.QCoreApplication.translate
        Form.setWindowTitle(_translate("Form", "Form"))
        self.label.setText(_translate("Form", "Ответ:"))

        self.answer.setText(self.ans)

    def get_answer(self):
        return [self.answer.text(), "__Entry__"]


class Answer_m(QtWidgets.QWidget):
    def __init__(self, answer, manswers):
        super(Answer_m, self).__init__()
        self.last_count = 0
        self.arr_mansevrs = []
        self.ans = answer
        self.manswers = manswers.split(":")
        self.setupUi(self)

    def setupUi(self, Form):
        Form.setObjectName("Form")
        Form.resize(411, 251)
        self.manswers_count = QtWidgets.QSpinBox(Form)
        self.manswers_count.setGeometry(QtCore.QRect(311, 10, 91, 22))
        self.manswers_count.setObjectName("manswers_count")
        self.verticalLayoutWidget = QtWidgets.QWidget(Form)
        self.verticalLayoutWidget.setGeometry(QtCore.QRect(10, 40, 391, 161))
        self.verticalLayoutWidget.setObjectName("verticalLayoutWidget")
        self.manswers_arr = QtWidgets.QVBoxLayout(self.verticalLayoutWidget)
        self.manswers_arr.setContentsMargins(0, 0, 0, 0)
        self.manswers_arr.setObjectName("manswers_arr")
        self.label = QtWidgets.QLabel(Form)
        self.label.setGeometry(QtCore.QRect(216, 10, 91, 21))
        self.label.setObjectName("label")
        self.label_2 = QtWidgets.QLabel(Form)
        self.label_2.setGeometry(QtCore.QRect(190, 210, 121, 21))
        self.label_2.setObjectName("label_2")
        self.try_answert_number = QtWidgets.QSpinBox(Form)
        self.try_answert_number.setGeometry(QtCore.QRect(311, 210, 91, 22))
        self.try_answert_number.setObjectName("try_answert_number")

        self.retranslateUi(Form)
        QtCore.QMetaObject.connectSlotsByName(Form)

    def retranslateUi(self, Form):
        _translate = QtCore.QCoreApplication.translate
        Form.setWindowTitle(_translate("Form", "Form"))
        self.label.setText(_translate("Form", "Кол-во вопросов"))
        self.label_2.setText(_translate("Form", "Номер верного ответа"))

        self.try_answert_number.setValue(int(self.ans))

        self.manswers_count.valueChanged.connect(self.remanswer)
        self.manswers_count.setValue(len(self.manswers))
        for i in range(len(self.arr_mansevrs)):
            self.arr_mansevrs[i].setText(self.manswers[i])

    def remanswer(self):
        if self.manswers_count.value() <= self.last_count:
            for i in range(self.last_count - self.manswers_count.value()):
                self.arr_mansevrs[-1].deleteLater()
                del self.arr_mansevrs[-1]
        else:
            for i in range(abs(self.last_count - self.manswers_count.value())):
                k = QtWidgets.QLineEdit(self)
                self.manswers_arr.addWidget(k)
                self.arr_mansevrs.append(k)
        self.last_count = self.manswers_count.value()

    def get_answer(self):
        return [str(self.try_answert_number.value()), ":".join([i.text() for i in self.arr_mansevrs])]