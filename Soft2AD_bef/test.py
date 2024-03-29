#!/usr/bin/env python
# coding: utf-8

# 예제 내용
# * QTreeWidget을 사용하여 아이템을 표시

__author__ = "Deokyu Lim <hong18s@gmail.com>"

from PyQt5.QtWidgets import QWidget
from PyQt5.QtWidgets import QFileDialog
from PyQt5.QtWidgets import QPushButton
from PyQt5.QtWidgets import QLabel
from PyQt5.QtWidgets import QPlainTextEdit
from PyQt5.QtWidgets import QApplication
from PyQt5.QtWidgets import QBoxLayout
from PyQt5.QtCore import Qt


class Form(QWidget):
    def __init__(self):
        QWidget.__init__(self, flags=Qt.Widget)
        self.setWindowTitle("QFileDialLog")
        box = QBoxLayout(QBoxLayout.TopToBottom)
        self.lb = QLabel()
        self.pb = QPushButton("Get full path of a file")
        self.plainText = QPlainTextEdit()
        self.pb2 = QPushButton("Get full path of a files")
        box.addWidget(self.lb)
        box.addWidget(self.pb)
        box.addWidget(self.plainText)
        box.addWidget(self.pb2)
        self.setLayout(box)
        self.pb.clicked.connect(self.get_file_name)
        self.pb2.clicked.connect(self.get_file_names)

    def get_file_name(self):
        filename = QFileDialog.getOpenFileName()
        self.lb.setText(filename[0])

    def get_file_names(self):
        filenames = QFileDialog.getOpenFileNames()
        st = ""
        for f in filenames[0]:
            st += f + "\n"
        self.plainText.setPlainText(st)


if __name__ == "__main__":
    import sys
    app = QApplication(sys.argv)
    form = Form()
    form.show()
    exit(app.exec_())