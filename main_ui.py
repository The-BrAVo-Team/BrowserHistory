import sys
from PySide6.QtWidgets import (QApplication, QWidget, QVBoxLayout, QLabel, QPushButton, 
                               QStackedWidget, QGroupBox, QGridLayout, QLineEdit, QComboBox,
                               QHBoxLayout, QTextEdit, QRadioButton, QButtonGroup, QMessageBox,
                               QFileDialog, QProgressBar)
from PySide6.QtCore import Slot, Qt, QTimer
from PySide6.QtGui import QPixmap
import re

# Import your project modules
from webcrawler import web_crawler
from accessHistory import fetch_history
from dateTime import create_date_time_output
from googleAutomate import GoogleAutomation

class StartMenu(QWidget):
    def __init__(self, stacked_widget):
        super().__init__()
        self.stacked_widget = stacked_widget
        self.initUI()

    def initUI(self):
        self.setWindowTitle("Start Menu")
        self.setGeometry(300, 100, 600, 400)  # Adjusted for better visual appearance

        layout = QVBoxLayout()
        
        # Adding a logo and background image
        self.logo_label = QLabel(self)
        self.logo_pixmap = QPixmap("web_crawler_logo.png")  
        self.logo_label.setPixmap(self.logo_pixmap)
        self.logo_label.setAlignment(Qt.AlignCenter)
        layout.addWidget(self.logo_label)
        
        # Adding welcome text
        self.label = QLabel("Welcome to Web Crawler", self)
        self.label.setAlignment(Qt.AlignCenter)
        self.label.setStyleSheet("font-size: 24px; font-weight: bold; color: white;")
        layout.addWidget(self.label)

        
        self.play_button = QPushButton("Start", self)
        self.play_button.setStyleSheet("""
            QPushButton {
                font-size: 18px;
                padding: 10px;
                background-color: #5cb85c;
                color: white;
                border-radius: 5px;
                margin: 10px 20px;
            }
            QPushButton:hover {
                background-color: #4cae4c;
            }
        """)
        self.play_button.clicked.connect(self.start_loading)

        layout.addStretch()
        layout.addWidget(self.play_button)
        layout.addStretch()

        self.progress_bar = QProgressBar(self)
        self.progress_bar.setVisible(False)
        layout.addWidget(self.progress_bar)
        
        self.loading_label = QLabel("Loading...", self)
        self.loading_label.setAlignment(Qt.AlignCenter)
        self.loading_label.setStyleSheet("font-size: 14px; color: white;")
        self.loading_label.setVisible(False)
        layout.addWidget(self.loading_label)

        self.setLayout(layout)

    @Slot()
    def start_loading(self):
        self.progress_bar.setVisible(True)
        self.loading_label.setVisible(True)
        self.progress_bar.setValue(0)
        self.timer = QTimer(self)
        self.timer.timeout.connect(self.update_progress)
        self.timer.start(50)  # Adjust the interval for the desired speed

    @Slot()
    def update_progress(self):
        value = self.progress_bar.value() + 1
        self.progress_bar.setValue(value)
        if value >= 100:
            self.timer.stop()
            self.open_main_app()

    @Slot()
    def open_main_app(self):
        self.progress_bar.setVisible(False)
        self.loading_label.setVisible(False)
        self.stacked_widget.setCurrentIndex(1)

class WebCrawlerApp(QWidget):
    def __init__(self, stacked_widget):
        super().__init__()
        self.stacked_widget = stacked_widget
        self.initUI()

    def initUI(self):
        self.setWindowTitle("Web Crawler App")
        self.setGeometry(300, 100, 600, 400)  # Adjusted for better visual appearance

        main_layout = QVBoxLayout()

        # Scenario Dropdown
        scenario_group = QGroupBox("Scenario Selection")
        scenario_layout = QVBoxLayout()

        self.scenario_label = QLabel("Scenario:")
        scenario_layout.addWidget(self.scenario_label)
        self.scenario_dropdown = QComboBox(self)
        self.scenario_dropdown.addItems(["clean", "ip", "hom", "cc", "drug"])
        scenario_layout.addWidget(self.scenario_dropdown)

        scenario_group.setLayout(scenario_layout)
        main_layout.addWidget(scenario_group)

        # Overwrite/Concatenate Radio Buttons
        operation_group = QGroupBox("Operation Mode")
        operation_layout = QHBoxLayout()

        self.radio_group = QButtonGroup(self)
        self.overwrite_radio = QRadioButton("Overwrite", self)
        self.concatenate_radio = QRadioButton("Concatenate", self)
        self.radio_group.addButton(self.overwrite_radio)
        self.radio_group.addButton(self.concatenate_radio)
        self.overwrite_radio.setChecked(True)

        operation_layout.addWidget(self.overwrite_radio)
        operation_layout.addWidget(self.concatenate_radio)
        operation_group.setLayout(operation_layout)
        main_layout.addWidget(operation_group)

        # Crawl Button and Result Display
        self.path_label = QLabel("Path:")
        main_layout.addWidget(self.path_label)
        self.path_entry = QLineEdit(self)
        main_layout.addWidget(self.path_entry)

        self.crawl_button = QPushButton("Crawl", self)
        self.crawl_button.setToolTip("Start crawling with GoogleAutomation")
        self.crawl_button.clicked.connect(self.run_google_automation)
        main_layout.addWidget(self.crawl_button)

        self.crawl_result = QTextEdit(self)
        self.crawl_result.setReadOnly(True)
        main_layout.addWidget(self.crawl_result)

        self.setLayout(main_layout)

        # Apply stylesheet for modern look
        self.setStyleSheet("""
            QWidget {
                font-size: 14px;
            }
            QGroupBox {
                font-weight: bold;
                border: 1px solid gray;
                border-radius: 5px;
                margin-top: 10px;
            }
            QGroupBox::title {
                subcontrol-origin: margin;
                subcontrol-position: top center;
                padding: 0 3px;
            }
            QPushButton {
                background-color: #5cb85c;
                color: white;
                border-radius: 5px;
                padding: 10px;
                margin-top: 10px;
            }
            QPushButton:hover {
                background-color: #4cae4c;
            }
            QLineEdit, QComboBox, QTextEdit {
                padding: 5px;
                border: 1px solid #ccc;
                border-radius: 5px;
            }
        """)

    def run_google_automation(self):
        path = self.path_entry.text()
        scenario = self.scenario_dropdown.currentText()
        overwrite = self.overwrite_radio.isChecked()

        if not path:
            QMessageBox.critical(self, "Error", "Please enter a valid path.")
            return

        # Clear the output box before running
        self.crawl_result.clear()

        # Run the GoogleAutomation with a log handler
        ga = GoogleAutomation(path, scenario, overwrite, log_output=self.log_output)
        ga.run()

    def log_output(self, message):
        """ Append log messages to the text box. """
        self.crawl_result.append(message)
        self.crawl_result.ensureCursorVisible()


if __name__ == "__main__":
    app = QApplication(sys.argv)

    stacked_widget = QStackedWidget()
    
    start_menu = StartMenu(stacked_widget)
    main_app = WebCrawlerApp(stacked_widget)

    stacked_widget.addWidget(start_menu)
    stacked_widget.addWidget(main_app)
    
    stacked_widget.setCurrentIndex(0)
    
    stacked_widget.show()
    sys.exit(app.exec())
