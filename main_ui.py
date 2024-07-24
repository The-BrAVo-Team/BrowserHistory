import sys
from PySide6.QtWidgets import (QApplication, QWidget, QVBoxLayout, QHBoxLayout,
                               QGridLayout, QPushButton, QLabel, QTextEdit, QLineEdit, 
                               QFileDialog, QMessageBox, QComboBox, QRadioButton, QButtonGroup)
from PySide6.QtCore import Slot

# Import your project modules
from webcrawler import web_crawler
from accessHistory import fetch_history
from dateTime import create_date_time_output
from googleAutomate import GoogleAutomation

class WebCrawlerApp(QWidget):
    def __init__(self):
        super().__init__()
        self.initUI()

    def initUI(self):
        self.setWindowTitle("Web Crawler App")
        self.setGeometry(300, 100, 800, 600)  # Set the window size and position

        main_layout = QVBoxLayout()

        # Date and Time Inputs
        date_time_layout = QGridLayout()

        self.start_date_label = QLabel("Start Date:")
        date_time_layout.addWidget(self.start_date_label, 0, 0)
        self.start_date_entry = QLineEdit(self)
        date_time_layout.addWidget(self.start_date_entry, 0, 1)

        self.end_date_label = QLabel("End Date:")
        date_time_layout.addWidget(self.end_date_label, 1, 0)
        self.end_date_entry = QLineEdit(self)
        date_time_layout.addWidget(self.end_date_entry, 1, 1)

        self.start_time_label = QLabel("Start Time:")
        date_time_layout.addWidget(self.start_time_label, 0, 2)
        self.start_time_entry = QLineEdit(self)
        date_time_layout.addWidget(self.start_time_entry, 0, 3)

        self.end_time_label = QLabel("End Time:")
        date_time_layout.addWidget(self.end_time_label, 1, 2)
        self.end_time_entry = QLineEdit(self)
        date_time_layout.addWidget(self.end_time_entry, 1, 3)

        main_layout.addLayout(date_time_layout)

        # Scenario Dropdown
        self.scenario_label = QLabel("Scenario:")
        main_layout.addWidget(self.scenario_label)
        self.scenario_dropdown = QComboBox(self)
        self.scenario_dropdown.addItems(["Scenario 1", "Scenario 2", "Scenario 3"])  # Add relevant scenarios
        main_layout.addWidget(self.scenario_dropdown)

        # Number of Records Dropdown
        self.records_label = QLabel("Number of Records:")
        main_layout.addWidget(self.records_label)
        self.records_dropdown = QComboBox(self)
        self.records_dropdown.addItems(["10", "20", "30", "40", "50"])  # Add relevant numbers
        main_layout.addWidget(self.records_dropdown)

        # Overwrite/Concatenate Radio Buttons
        self.radio_group = QButtonGroup(self)
        self.overwrite_radio = QRadioButton("Overwrite", self)
        self.concatenate_radio = QRadioButton("Concatenate", self)
        self.radio_group.addButton(self.overwrite_radio)
        self.radio_group.addButton(self.concatenate_radio)
        self.overwrite_radio.setChecked(True)

        radio_layout = QHBoxLayout()
        radio_layout.addWidget(self.overwrite_radio)
        radio_layout.addWidget(self.concatenate_radio)
        main_layout.addLayout(radio_layout)

        # Crawl Button and Result Display
        self.crawl_button = QPushButton("Crawl", self)
        self.crawl_button.clicked.connect(self.crawl_url)
        main_layout.addWidget(self.crawl_button)

        self.crawl_result = QTextEdit(self)
        main_layout.addWidget(self.crawl_result)

        self.setLayout(main_layout)

    @Slot()
    def crawl_url(self):
        url = self.url_entry.text()
        if url:
            links = web_crawler(url)
            self.crawl_result.clear()
            for link in links:
                self.crawl_result.append(link)
        else:
            QMessageBox.critical(self, "Error", "Please enter a URL.")

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
    window = WebCrawlerApp()
    window.show()
    sys.exit(app.exec())