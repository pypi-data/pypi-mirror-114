#!/usr/bin/env python
# -*- encoding: utf-8 -*-
"""
@File    :  main.py
@Date    :  2021/07/23
@Author  :  Yaronzz
@Version :  1.0
@Contact :  yaronhuang@foxmail.com
@Desc    :  
"""
from PyQt5.QtWidgets import QWidget, QPushButton, QLineEdit, QInputDialog, QLabel, QTableView, QGridLayout


class MainView(QWidget):

    def __init__(self):
        super().__init__()
        self.__initView__()

    def __initView__(self):
        self.label0 = QLabel("From bdy:")
        self.label1 = QLabel("  To aly:")

        self.edit0 = QLineEdit(self)
        self.edit0.setEnabled(False)
        self.edit1 = QLineEdit(self)

        self.btn0 = QPushButton('UP', self)
        self.btn0.clicked.connect(self.__upSlot__)
        self.btn1 = QPushButton('RUN', self)
        self.btn1.clicked.connect(self.__runSlot__)

        self.tableView = QTableView(self)

        self.layout = QGridLayout()
        self.layout.addWidget(self.label0, 0, 0)
        self.layout.addWidget(self.edit0, 0, 1)
        self.layout.addWidget(self.btn0, 0, 2)
        self.layout.addWidget(self.tableView, 1, 0, 1, 3)
        self.layout.addWidget(self.label0, 2, 0)
        self.layout.addWidget(self.edit0, 2, 1)
        self.layout.addWidget(self.btn0, 3, 2)

        self.setGeometry(300, 300, 290, 150)
        self.setWindowTitle('Input dialog')
        self.show()

    def __upSlot__(self):
        pass

    def __runSlot__(self):
        pass

    def showDialog(self):
        text, ok = QInputDialog.getText(self, 'Input Dialog',
                                        'Enter your name:')

        if ok:
            self.le.setText(str(text))