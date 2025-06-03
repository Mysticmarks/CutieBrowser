# -*- coding: utf-8 -*-
"""
Created on Sun Apr 21 10:07:22 2024

@author: mysticmarks
"""

import sys
import logging # Added for logging
from PyQt5.QtWidgets import QApplication, QMainWindow, QLineEdit, QTabWidget, QVBoxLayout, QWidget, QAction, QFileDialog, QMessageBox, QPushButton, QHBoxLayout
from PyQt5.QtWebEngineWidgets import QWebEngineView, QWebEnginePage
from PyQt5.QtCore import QUrl, QCoreApplication, Qt

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

        # Add 'New Tab' button
        new_tab_button = QPushButton("+")
        new_tab_button.setMaximumWidth(30)
        new_tab_button.clicked.connect(lambda: self.add_tab()) # Connect to existing add_tab
        self.tabs.setCornerWidget(new_tab_button, Qt.TopRightCorner)

        # Enable closable tabs
        self.tabs.setTabsClosable(True)
        self.tabs.tabCloseRequested.connect(self.close_tab)
        self.tabs.currentChanged.connect(self.update_navigation_buttons) # Update nav buttons on tab change

        # Navigation buttons
        nav_layout = QHBoxLayout()
        self.back_button = QPushButton("<-")
        self.back_button.clicked.connect(self.go_back)
        self.forward_button = QPushButton("->")
        self.forward_button.clicked.connect(self.go_forward)
        self.refresh_button = QPushButton("R")
        self.refresh_button.clicked.connect(self.refresh_page)

        nav_layout.addWidget(self.back_button)
        nav_layout.addWidget(self.forward_button)
        nav_layout.addWidget(self.refresh_button)
        self.layout.addLayout(nav_layout) # Add nav buttons layout

        self.url_bar = QLineEdit()
        self.url_bar.returnPressed.connect(self.navigate_to_url)
        self.layout.addWidget(self.url_bar)

        self.add_tab("https://www.google.com") # This will also log

        self.init_menu_bar()
        self.update_navigation_buttons() # Initial state update
        # logging.info("CutieBrowser window initialized") # Optional, app start is logged

    def go_back(self):
        current_browser = self.tabs.currentWidget()
        if current_browser:
            logging.info("Navigating back")
            current_browser.back()

    def go_forward(self):
        current_browser = self.tabs.currentWidget()
        if current_browser:
            logging.info("Navigating forward")
            current_browser.forward()

    def refresh_page(self):
        current_browser = self.tabs.currentWidget()
        if current_browser:
            logging.info("Refreshing page")
            current_browser.reload()

    def update_navigation_buttons(self):
        current_browser = self.tabs.currentWidget()
        if current_browser:
            self.back_button.setEnabled(current_browser.page().action(QWebEnginePage.Back).isEnabled())
            self.forward_button.setEnabled(current_browser.page().action(QWebEnginePage.Forward).isEnabled())
            self.refresh_button.setEnabled(True) # Refresh is always possible if there's a tab
        else:
            self.back_button.setEnabled(False)
            self.forward_button.setEnabled(False)
            self.refresh_button.setEnabled(False)

    def close_tab(self, index):
        logging.info(f"Closing tab at index {index}")
        widget = self.tabs.widget(index)
        if widget:
            widget.deleteLater()
        self.tabs.removeTab(index)
        self.update_navigation_buttons() # Update nav buttons after closing a tab

    def add_tab(self, url=None):
        browser = QWebEngineView()
        browser.setPage(QWebEnginePage())
        browser.loadFinished.connect(lambda ok, b=browser: self.handle_load_finished(ok, b))
        browser.page().urlChanged.connect(lambda url, browser=browser: self.update_url_bar(url, browser))
        browser.page().profile().downloadRequested.connect(self.download_requested)

        if url:
            logging.info(f"Adding new tab with URL: {url}")
            browser.load(QUrl(url))
        else:
            logging.info("Adding new empty tab")
            # Load a default page for empty tabs, e.g., about:blank or a custom local page
            # browser.load(QUrl("about:blank")) # Or your preferred default

        self.tabs.addTab(browser, "New Tab") # Add tab after attempting to load URL or setting default
        self.update_navigation_buttons() # Update nav buttons after adding a new tab

    def navigate_to_url(self):
        url = self.url_bar.text()
        logging.info(f"Navigating to URL from bar: {url}")
        if not url.startswith("http://") and not url.startswith("https://"):
            url = "https://" + url
            logging.info(f"URL modified to: {url}") # Log modification
        self.add_tab(url) # add_tab will log the specifics of adding the tab

    def update_url_bar(self, url, browser):
        index = self.tabs.indexOf(browser)
        # It's possible the tab is closed before this callback, check index
        if index != -1:
            self.tabs.setTabText(index, url.toString())
        self.url_bar.setText(url.toString())

    def download_requested(self, download):
        file_path, _ = QFileDialog.getSaveFileName(self, "Save File", "", "All Files (*)")
        if file_path:
            logging.info(f"Download requested: {download.url().toString()} to {file_path}")
            download.setPath(file_path)
            download.accept()
        else:
            logging.info(f"Download cancelled for: {download.url().toString()}")
            download.cancel()


    def init_menu_bar(self):
        menu_bar = self.menuBar() # Corrected typo here: menu_.bar to menu_bar

        file_menu = menu_bar.addMenu("File")
        new_tab_action = QAction("New Tab", self)
        new_tab_action.triggered.connect(lambda: self.add_tab()) # add_tab will log
        file_menu.addAction(new_tab_action)

        exit_action = QAction("Exit", self)
        exit_action.triggered.connect(self.close)
        file_menu.addAction(exit_action)

        help_menu = menu_bar.addMenu("Help")
        about_action = QAction("About", self)
        about_action.triggered.connect(self.show_about_dialog)
        help_menu.addAction(about_action)

    def show_about_dialog(self):
        logging.info("Showing About dialog.")
        QMessageBox.about(self, "About Cutie Browser", "Cutie Browser - A Simple Web Browser built with PyQt5")

    def handle_load_finished(self, ok, browser_instance):
        page_url = browser_instance.url().toString()
        if not ok:
            logging.error(f"Failed to load page: {page_url}")
            QMessageBox.warning(self, "Load Error", f"Failed to load page: {page_url}. Please check the URL and your internet connection.")
        else:
            logging.info(f"Successfully loaded page: {page_url}")
        self.update_navigation_buttons() # Update nav buttons after page load attempt


if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO,
                        format='%(asctime)s - %(levelname)s - %(message)s',
                        handlers=[logging.FileHandler("cutiebrowser.log"),
                                  logging.StreamHandler()])
    logging.info("Application started")

    app = QApplication(sys.argv)
    browser = CutieBrowser()
    browser.show()
    sys.exit(app.exec_())
