import sys
from PySide6.QtWidgets import (QApplication, QWidget, QVBoxLayout, QLabel, QPushButton, 
                               QStackedWidget, QGroupBox, QGridLayout, QLineEdit, QComboBox,
                               QHBoxLayout, QTextEdit, QRadioButton, QButtonGroup, QMessageBox,
                               QFileDialog)
from PySide6.QtCore import Slot, Qt
from PySide6.QtGui import QPixmap

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
        self.setGeometry(300, 100, 400, 300)

        layout = QVBoxLayout()
        
        # Adding a logo and background image
        self.logo_label = QLabel(self)
        self.logo_pixmap = QPixmap("web_crawler_logo.png")  
        self.logo_label.setPixmap(self.logo_pixmap)
        self.logo_label.setAlignment(Qt.AlignCenter)
        layout.addWidget(self.logo_label)
        
        # Adding welcome text
        self.label = QLabel("Welcome to Browser_Gen", self)
        self.label.setAlignment(Qt.AlignCenter)
        self.label.setStyleSheet("font-size: 24px; font-weight: bold; color: #f5f5f5;")
        
        self.play_button = QPushButton("Start", self)
        self.play_button.setStyleSheet("""
            QPushButton {
                font-size: 18px;
                padding: 10px;
                background-color: #5cb85c;
                color: white;
                border-radius: 5px;
            }
            QPushButton:hover {
                background-color: #4cae4c;
            }
        """)
        self.play_button.clicked.connect(self.open_main_app)

        layout.addWidget(self.label)
        layout.addStretch()
        layout.addWidget(self.play_button)
        layout.addStretch()

        self.setLayout(layout)


    @Slot()
    def open_main_app(self):
        self.stacked_widget.setCurrentIndex(1)

class WebCrawlerApp(QWidget):
    def __init__(self, stacked_widget):
        super().__init__()
        self.stacked_widget = stacked_widget
        self.initUI()

    def initUI(self):
        self.setWindowTitle("Web Crawler App")
        self.setGeometry(300, 100, 400, 300)

        main_layout = QVBoxLayout()

        # Date and Time Inputs
        date_time_group = QGroupBox("Date and Time Configuration")
        date_time_layout = QGridLayout()

        self.start_date_label = QLabel("Start Date:")
        date_time_layout.addWidget(self.start_date_label, 0, 0)
        self.start_date_entry = QLineEdit(self)
        self.start_date_entry.setPlaceholderText("yyyy-mm-dd")
        date_time_layout.addWidget(self.start_date_entry, 0, 1)

        self.end_date_label = QLabel("End Date:")
        date_time_layout.addWidget(self.end_date_label, 1, 0)
        self.end_date_entry = QLineEdit(self)
        self.end_date_entry.setPlaceholderText("yyyy-mm-dd")
        date_time_layout.addWidget(self.end_date_entry, 1, 1)

        self.start_time_label = QLabel("Start Time:")
        date_time_layout.addWidget(self.start_time_label, 0, 2)
        self.start_time_entry = QLineEdit(self)
        self.start_time_entry.setPlaceholderText("HH:MM:SS")
        date_time_layout.addWidget(self.start_time_entry, 0, 3)

        self.end_time_label = QLabel("End Time:")
        date_time_layout.addWidget(self.end_time_label, 1, 2)
        self.end_time_entry = QLineEdit(self)
        self.end_time_entry.setPlaceholderText("HH:MM:SS")
        date_time_layout.addWidget(self.end_time_entry, 1, 3)

        date_time_group.setLayout(date_time_layout)
        main_layout.addWidget(date_time_group)

        # Scenario Dropdown
        scenario_group = QGroupBox("Scenario Selection")
        scenario_layout = QVBoxLayout()

        self.scenario_label = QLabel("Scenario:")
        scenario_layout.addWidget(self.scenario_label)
        self.scenario_dropdown = QComboBox(self)
        self.scenario_dropdown.addItems(["IP Theft", "Clean", "Homicide", "Narcotics", "Child Corn"])
        scenario_layout.addWidget(self.scenario_dropdown)

        scenario_group.setLayout(scenario_layout)
        main_layout.addWidget(scenario_group)

        # Number of Records Dropdown
        records_group = QGroupBox("Record Configuration")
        records_layout = QVBoxLayout()

        self.records_label = QLabel("Number of Records:")
        records_layout.addWidget(self.records_label)
        self.records_dropdown = QComboBox(self)
        self.records_dropdown.addItems(["1000", "1500", "2000"])
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
        self.crawl_button = QPushButton("Crawl", self)
        self.crawl_button.setToolTip("Start crawling the provided URL")
        self.crawl_button.clicked.connect(self.run_automation)
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

    @Slot()
    def crawl_url(self):
        #
        # ["IP Theft", "Clean", "Homicide", "Narcotics", "Child Corn"]
        scenarios = {
            "IP Theft" : "ip",
            "Clean" : "clean",
            "Homicide" : "hom",
            "Narcotics" : "drug",
            "Child Corn" : "cc"
        }
        

    @Slot()
    def fetch_history(self):
        history = fetch_history()
        self.history_result.clear()
        for entry in history:
            self.history_result.append(entry)

    @Slot()
    def generate_datetime(self):
        self.start_date = self.start_date_entry.text()
        self.end_date = self.end_date_entry.text()
        self.start_time = self.start_time_entry.text()
        self.end_time = self.end_time_entry.text()
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
        scenarios = {
            "IP Theft" : "ip",
            "Clean" : "clean",
            "Homicide" : "hom",
            "Narcotics" : "drug",
            "Child Corn" : "cc"
        }
        start_date = self.start_date_entry.text()
        end_date = self.end_date_entry.text()
        start_time = self.start_time_entry.text()
        end_time = self.end_time_entry.text()
        if start_date and end_date and start_time and end_time:
            QMessageBox.information(self, "One Last Step", "Press ok to run Google Automation. This may take up to 15 minutes.")
            ga = GoogleAutomation( scenarios[self.scenario_dropdown.currentText()], start_date, end_date, start_time, end_time, overwrite=True)
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
