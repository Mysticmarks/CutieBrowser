# -*- coding: utf-8 -*-
"""
Created on Sun Apr 21 10:07:22 2024

@author: mysticmarks
"""

import sys
from PyQt5.QtWidgets import QApplication, QMainWindow, QLineEdit, QTabWidget, QVBoxLayout, QWidget, QAction, QFileDialog, QMessageBox
from PyQt5.QtWebEngineWidgets import QWebEngineView, QWebEnginePage
from PyQt5.QtCore import QUrl, QCoreApplication

class CutieBrowser(QMainWindow):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("Cutie Browser")
        self.setGeometry(100, 100, 800, 600)

        self.central_widget = QWidget()
        self.layout = QVBoxLayout()
        self.central_widget.setLayout(self.layout)
        self.setCentralWidget(self.central_widget)

        self.tabs = QTabWidget()
        self.layout.addWidget(self.tabs)

        self.add_tab("https://www.google.com")

        self.url_bar = QLineEdit()
        self.url_bar.returnPressed.connect(self.navigate_to_url)
        self.layout.addWidget(self.url_bar)

        self.init_menu_bar()

    def add_tab(self, url=None):
        browser = QWebEngineView()
        browser.setPage(QWebEnginePage())
        browser.page().urlChanged.connect(lambda url, browser=browser: self.update_url_bar(url, browser))
        browser.page().profile().downloadRequested.connect(self.download_requested)
        self.tabs.addTab(browser, "New Tab")
        if url:
            browser.load(QUrl(url))

    def navigate_to_url(self):
        url = self.url_bar.text()
        if not url.startswith("http"):
            url = "http://" + url
        self.add_tab(url)

    def update_url_bar(self, url, browser):
        index = self.tabs.indexOf(browser)
        self.tabs.setTabText(index, url.toString())
        self.url_bar.setText(url.toString())

    def download_requested(self, download):
        file_path, _ = QFileDialog.getSaveFileName(self, "Save File", "", "All Files (*)")
        if file_path:
            download.setPath(file_path)
            download.accept()

    def init_menu_bar(self):
        menu_bar = self.menuBar()

        file_menu = menu_bar.addMenu("File")
        new_tab_action = QAction("New Tab", self)
        new_tab_action.triggered.connect(lambda: self.add_tab())
        file_menu.addAction(new_tab_action)

        exit_action = QAction("Exit", self)
        exit_action.triggered.connect(self.close)
        file_menu.addAction(exit_action)

        help_menu = menu_bar.addMenu("Help")
        about_action = QAction("About", self)
        about_action.triggered.connect(self.show_about_dialog)
        help_menu.addAction(about_action)

    def show_about_dialog(self):
        QMessageBox.about(self, "About Cutie Browser", "Cutie Browser - A Simple Web Browser built with PyQt5")

if __name__ == "__main__":
    app = QApplication(sys.argv)
    browser = CutieBrowser()
    browser.show()
    sys.exit(app.exec_())
