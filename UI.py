import tkinter as tk
from tkinter import filedialog, messagebox
from webcrawler import web_crawler, read_urls_from_file
from accessHistory import fetch_history
from dateTime import create_date_time_output
from googleAutomate import GoogleAutomation

class WebCrawlerApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Web Crawler App")
        self.create_widgets()

    def create_widgets(self):
        # Frame for web crawler
        self.crawler_frame = tk.LabelFrame(self.root, text="Web Crawler", padx=10, pady=10)
        self.crawler_frame.pack(padx=10, pady=10)

        self.url_label = tk.Label(self.crawler_frame, text="URL:")
        self.url_label.grid(row=0, column=0)
        self.url_entry = tk.Entry(self.crawler_frame, width=50)
        self.url_entry.grid(row=0, column=1)

        self.crawl_button = tk.Button(self.crawler_frame, text="Crawl", command=self.crawl_url)
        self.crawl_button.grid(row=0, column=2)

        self.crawl_result = tk.Text(self.crawler_frame, height=10, width=70)
        self.crawl_result.grid(row=1, column=0, columnspan=3, pady=10)

        # Frame for accessing history
        self.history_frame = tk.LabelFrame(self.root, text="Access History", padx=10, pady=10)
        self.history_frame.pack(padx=10, pady=10)

        self.history_button = tk.Button(self.history_frame, text="Fetch History", command=self.fetch_history)
        self.history_button.pack()

        self.history_result = tk.Text(self.history_frame, height=10, width=70)
        self.history_result.pack(pady=10)

        # Frame for date and time generation
        self.datetime_frame = tk.LabelFrame(self.root, text="Date Time Generation", padx=10, pady=10)
        self.datetime_frame.pack(padx=10, pady=10)

        self.start_date_label = tk.Label(self.datetime_frame, text="Start Date (YYYY-MM-DD):")
        self.start_date_label.grid(row=0, column=0)
        self.start_date_entry = tk.Entry(self.datetime_frame)
        self.start_date_entry.grid(row=0, column=1)

        self.end_date_label = tk.Label(self.datetime_frame, text="End Date (YYYY-MM-DD):")
        self.end_date_label.grid(row=1, column=0)
        self.end_date_entry = tk.Entry(self.datetime_frame)
        self.end_date_entry.grid(row=1, column=1)

        self.start_time_label = tk.Label(self.datetime_frame, text="Start Time (HH:MM:SS):")
        self.start_time_label.grid(row=2, column=0)
        self.start_time_entry = tk.Entry(self.datetime_frame)
        self.start_time_entry.grid(row=2, column=1)

        self.end_time_label = tk.Label(self.datetime_frame, text="End Time (HH:MM:SS):")
        self.end_time_label.grid(row=3, column=0)
        self.end_time_entry = tk.Entry(self.datetime_frame)
        self.end_time_entry.grid(row=3, column=1)

        self.generate_button = tk.Button(self.datetime_frame, text="Generate", command=self.generate_datetime)
        self.generate_button.grid(row=4, column=0, columnspan=2, pady=10)

        self.datetime_result = tk.Text(self.datetime_frame, height=10, width=70)
        self.datetime_result.grid(row=5, column=0, columnspan=2)

        # Frame for Google automation
        self.automation_frame = tk.LabelFrame(self.root, text="Google Automation", padx=10, pady=10)
        self.automation_frame.pack(padx=10, pady=10)

        self.path_label = tk.Label(self.automation_frame, text="Profile Path:")
        self.path_label.grid(row=0, column=0)
        self.path_entry = tk.Entry(self.automation_frame, width=50)
        self.path_entry.grid(row=0, column=1)

        self.keyword_label = tk.Label(self.automation_frame, text="Keywords File:")
        self.keyword_label.grid(row=1, column=0)
        self.keyword_button = tk.Button(self.automation_frame, text="Browse", command=self.browse_keywords)
        self.keyword_button.grid(row=1, column=2)
        self.keyword_file = tk.Label(self.automation_frame, text="")
        self.keyword_file.grid(row=1, column=1)

        self.search_engine_label = tk.Label(self.automation_frame, text="Search Engines File:")
        self.search_engine_label.grid(row=2, column=0)
        self.search_engine_button = tk.Button(self.automation_frame, text="Browse", command=self.browse_search_engines)
        self.search_engine_button.grid(row=2, column=2)
        self.search_engine_file = tk.Label(self.automation_frame, text="")
        self.search_engine_file.grid(row=2, column=1)

        self.automation_button = tk.Button(self.automation_frame, text="Run Automation", command=self.run_automation)
        self.automation_button.grid(row=3, column=0, columnspan=3, pady=10)

    def crawl_url(self):
        url = self.url_entry.get()
        if url:
            links = web_crawler(url)
            self.crawl_result.delete(1.0, tk.END)
            for link in links:
                self.crawl_result.insert(tk.END, f"{link}\n")
        else:
            messagebox.showerror("Error", "Please enter a URL.")

    def fetch_history(self):
        history = fetch_history()
        self.history_result.delete(1.0, tk.END)
        for entry in history:
            self.history_result.insert(tk.END, f"{entry}\n")

    def generate_datetime(self):
        start_date = self.start_date_entry.get()
        end_date = self.end_date_entry.get()
        start_time = self.start_time_entry.get()
        end_time = self.end_time_entry.get()
        if start_date and end_date and start_time and end_time:
            datetimes = create_date_time_output(start_date, end_date, start_time, end_time)
            self.datetime_result.delete(1.0, tk.END)
            for dt in datetimes:
                self.datetime_result.insert(tk.END, f"{dt}\n")
        else:
            messagebox.showerror("Error", "Please fill in all date and time fields.")

    def browse_keywords(self):
        file_path = filedialog.askopenfilename(filetypes=[("Text files", "*.txt")])
        if file_path:
            self.keyword_file.config(text=file_path)

    def browse_search_engines(self):
        file_path = filedialog.askopenfilename(filetypes=[("Text files", "*.txt")])
        if file_path:
            self.search_engine_file.config(text=file_path)

    def run_automation(self):
        path = self.path_entry.get()
        keyword_file = self.keyword_file.cget("text")
        search_engine_file = self.search_engine_file.cget("text")
        if path and keyword_file and search_engine_file:
            ga = GoogleAutomation(path, keyword_file, search_engine_file)
            ga.run()
            messagebox.showinfo("Success", "Google automation completed.")
        else:
            messagebox.showerror("Error", "Please fill in all fields and select the necessary files.")

if __name__ == "__main__":
    root = tk.Tk()
    app = WebCrawlerApp(root)
    root.mainloop()
