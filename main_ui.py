import sys
from PySide6.QtWidgets import (QApplication, QWidget, QVBoxLayout, QHBoxLayout,
                               QPushButton, QLabel, QTextEdit, QLineEdit, QFileDialog, QMessageBox)
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

        # Layout for web crawler
        self.crawler_layout = QVBoxLayout()

        self.url_label = QLabel("URL:")
        self.crawler_layout.addWidget(self.url_label)

        self.url_entry = QLineEdit(self)
        self.crawler_layout.addWidget(self.url_entry)

        self.crawl_button = QPushButton("Crawl", self)
        self.crawl_button.clicked.connect(self.crawl_url)
        self.crawler_layout.addWidget(self.crawl_button)

        self.crawl_result = QTextEdit(self)
        self.crawler_layout.addWidget(self.crawl_result)

        # Layout for access history
        self.history_layout = QVBoxLayout()

        self.history_button = QPushButton("Fetch History", self)
        self.history_button.clicked.connect(self.fetch_history)
        self.history_layout.addWidget(self.history_button)

        self.history_result = QTextEdit(self)
        self.history_layout.addWidget(self.history_result)

        # Layout for date and time generation
        self.datetime_layout = QVBoxLayout()

        self.start_date_label = QLabel("Start Date (YYYY-MM-DD):")
        self.datetime_layout.addWidget(self.start_date_label)

        self.start_date_entry = QLineEdit(self)
        self.datetime_layout.addWidget(self.start_date_entry)

        self.end_date_label = QLabel("End Date (YYYY-MM-DD):")
        self.datetime_layout.addWidget(self.end_date_label)

        self.end_date_entry = QLineEdit(self)
        self.datetime_layout.addWidget(self.end_date_entry)

        self.start_time_label = QLabel("Start Time (HH:MM:SS):")
        self.datetime_layout.addWidget(self.start_time_label)

        self.start_time_entry = QLineEdit(self)
        self.datetime_layout.addWidget(self.start_time_entry)

        self.end_time_label = QLabel("End Time (HH:MM:SS):")
        self.datetime_layout.addWidget(self.end_time_label)

        self.end_time_entry = QLineEdit(self)
        self.datetime_layout.addWidget(self.end_time_entry)

        self.generate_button = QPushButton("Generate", self)
        self.generate_button.clicked.connect(self.generate_datetime)
        self.datetime_layout.addWidget(self.generate_button)

        self.datetime_result = QTextEdit(self)
        self.datetime_layout.addWidget(self.datetime_result)

        # Layout for Google automation
        self.automation_layout = QVBoxLayout()

        self.path_label = QLabel("Profile Path:")
        self.automation_layout.addWidget(self.path_label)

        self.path_entry = QLineEdit(self)
        self.automation_layout.addWidget(self.path_entry)

        self.keyword_label = QLabel("Keywords File:")
        self.automation_layout.addWidget(self.keyword_label)

        self.keyword_button = QPushButton("Browse", self)
        self.keyword_button.clicked.connect(self.browse_keywords)
        self.automation_layout.addWidget(self.keyword_button)

        self.keyword_file = QLabel(self)
        self.automation_layout.addWidget(self.keyword_file)

        self.search_engine_label = QLabel("Search Engines File:")
        self.automation_layout.addWidget(self.search_engine_label)

        self.search_engine_button = QPushButton("Browse", self)
        self.search_engine_button.clicked.connect(self.browse_search_engines)
        self.automation_layout.addWidget(self.search_engine_button)

        self.search_engine_file = QLabel(self)
        self.automation_layout.addWidget(self.search_engine_file)

        self.automation_button = QPushButton("Run Automation", self)
        self.automation_button.clicked.connect(self.run_automation)
        self.automation_layout.addWidget(self.automation_button)

        # Main layout
        self.main_layout = QVBoxLayout()

        self.main_layout.addLayout(self.crawler_layout)
        self.main_layout.addLayout(self.history_layout)
        self.main_layout.addLayout(self.datetime_layout)
        self.main_layout.addLayout(self.automation_layout)

        self.setLayout(self.main_layout)

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
