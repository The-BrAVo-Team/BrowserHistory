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

        # Date and Time Inputs
        date_time_group = QGroupBox("Date and Time Configuration")
        date_time_layout = QGridLayout()

        self.start_date_label = QLabel("Start Date (YYYY-MM-DD):")
        date_time_layout.addWidget(self.start_date_label, 0, 0)
        self.start_date_entry = QLineEdit(self)
        date_time_layout.addWidget(self.start_date_entry, 0, 1)

        self.end_date_label = QLabel("End Date (YYYY-MM-DD):")
        date_time_layout.addWidget(self.end_date_label, 1, 0)
        self.end_date_entry = QLineEdit(self)
        date_time_layout.addWidget(self.end_date_entry, 1, 1)

        self.start_time_label = QLabel("Start Time (HH:MM):")
        date_time_layout.addWidget(self.start_time_label, 0, 2)
        self.start_time_entry = QLineEdit(self)
        date_time_layout.addWidget(self.start_time_entry, 0, 3)

        self.end_time_label = QLabel("End Time (HH:MM):")
        date_time_layout.addWidget(self.end_time_label, 1, 2)
        self.end_time_entry = QLineEdit(self)
        date_time_layout.addWidget(self.end_time_entry, 1, 3)

        date_time_group.setLayout(date_time_layout)
        main_layout.addWidget(date_time_group)

        # Scenario Dropdown
        scenario_group = QGroupBox("Scenario Selection")
        scenario_layout = QVBoxLayout()

        self.scenario_label = QLabel("Scenario:")
        scenario_layout.addWidget(self.scenario_label)
        self.scenario_dropdown = QComboBox(self)
        self.scenario_dropdown.addItems(["Scenario 1", "Scenario 2", "Scenario 3"])
        scenario_layout.addWidget(self.scenario_dropdown)

        scenario_group.setLayout(scenario_layout)
        main_layout.addWidget(scenario_group)

        # Number of Records Dropdown
        records_group = QGroupBox("Record Configuration")
        records_layout = QVBoxLayout()

        self.records_label = QLabel("Number of Records:")
        records_layout.addWidget(self.records_label)
        self.records_dropdown = QComboBox(self)
        self.records_dropdown.addItems(["10", "20", "30", "40", "50"])
        records_layout.addWidget(self.records_dropdown)

        records_group.setLayout(records_layout)
        main_layout.addWidget(records_group)

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
        self.url_label = QLabel("Enter URL:")
        main_layout.addWidget(self.url_label)
        self.url_entry = QLineEdit(self)
        main_layout.addWidget(self.url_entry)

        self.crawl_button = QPushButton("Crawl", self)
        self.crawl_button.setToolTip("Start crawling the provided URL")
        self.crawl_button.clicked.connect(self.crawl_url)
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

    def validate_date(self, date_str):
        return re.match(r'^\d{4}-\d{2}-\d{2}$', date_str)

    def validate_time(self, time_str):
        return re.match(r'^\d{2}:\d{2}$', time_str)

    def validate_url(self, url_str):
        return re.match(r'^https?:\/\/', url_str)

    @Slot()
    def crawl_url(self):
        url = self.url_entry.text()
        start_date = self.start_date_entry.text()
        end_date = self.end_date_entry.text()
        start_time = self.start_time_entry.text()
        end_time = self.end_time_entry.text()

        if not self.validate_url(url):
            QMessageBox.critical(self, "Error", "Please enter a valid URL.")
            return

        if not (self.validate_date(start_date) and self.validate_date(end_date)):
            QMessageBox.critical(self, "Error", "Please enter valid dates in YYYY-MM-DD format.")
            return

        if not (self.validate_time(start_time) and self.validate_time(end_time)):
            QMessageBox.critical(self, "Error", "Please enter valid times in HH:MM format.")
            return

        # Assuming other necessary input fields are already validated

        links = web_crawler(url)
        self.crawl_result.clear()
        for link in links:
            self.crawl_result.append(link)

    @Slot()
    def fetch_history(self):
        history = fetch_history()
        self.history_result.clear()
        for entry in history:
            self.history_result.append(entry)

    @Slot()
    def generate_datetime(self):
        start_date = self.start_date_entry.text()
        end_date = self.end_date_entry.text()
        start_time = self.start_time_entry.text()
        end_time = self.end_time_entry.text()

        if not (self.validate_date(start_date) and self.validate_date(end_date)):
            QMessageBox.critical(self, "Error", "Please enter valid dates in YYYY-MM-DD format.")
            return

        if not (self.validate_time(start_time) and self.validate_time(end_time)):
            QMessageBox.critical(self, "Error", "Please enter valid times in HH:MM format.")
            return

        if start_date and end_date and start_time and end_time:
            datetimes = create_date_time_output(start_date, end_date, start_time, end_time)
            self.datetime_result.clear()
            for dt in datetimes:
                self.datetime_result.append(dt)
        else:
            QMessageBox.critical(self, "Error", "Please fill in all date and time fields.")

    @Slot()
    def browse_keywords(self):
        file_path, _ = QFileDialog.getOpenFileName(self, "Select Keywords File", "", "Text files (*.txt)")
        if file_path:
            self.keyword_file.setText(file_path)

    @Slot()
    def browse_search_engines(self):
        file_path, _ = QFileDialog.getOpenFileName(self, "Select Search Engines File", "", "Text files (*.txt)")
        if file_path:
            self.search_engine_file.setText(file_path)

    @Slot()
    def run_automation(self):
        path = self.path_entry.text()
        keyword_file = self.keyword_file.text()
        search_engine_file = self.search_engine_file.text()
        if path and keyword_file and search_engine_file:
            ga = GoogleAutomation(path, keyword_file, search_engine_file)
            ga.run()
            QMessageBox.information(self, "Success", "Google automation completed.")
        else:
            QMessageBox.critical(self, "Error", "Please fill in all fields and select the necessary files.")

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
