import tkinter as tk
from tkinter import ttk, filedialog, messagebox
import requests
import time
import threading
import csv
import os
import shutil
from datetime import datetime, timezone

class APIPollingGUI:
    def __init__(self, root):
        self.root = root
        self.root.title("Easy Polling v1.0 - API Data Polling Tool")
        self.root.geometry("600x550")
        
        # Variables
        self.polling_active = False
        self.polling_thread = None
        self.start_time = None
        self.csv_filepath = None
        
        self.setup_ui()
        
    def setup_ui(self):
        # Main frame
        main_frame = ttk.Frame(self.root, padding="20")
        main_frame.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))
        
        # Title and header
        title_label = ttk.Label(main_frame, text="Easy Polling", 
                               font=('Arial', 18, 'bold'))
        title_label.grid(row=0, column=0, columnspan=2, pady=(0, 5))
        
        subtitle_label = ttk.Label(main_frame, text="API Data Polling Tool v1.0", 
                                  font=('Arial', 12))
        subtitle_label.grid(row=1, column=0, columnspan=2, pady=(0, 10))
        
        # Author info
        # author_frame = ttk.Frame(main_frame)
        # author_frame.grid(row=2, column=0, columnspan=2, pady=(0, 15))
        
        # author_label = ttk.Label(author_frame, text="Made by: ", font=('Arial', 9))
        # author_label.grid(row=0, column=0)
        
        # author_link = ttk.Label(author_frame, text="Rajesh Paul", 
        #                        font=('Arial', 9, 'underline'), 
        #                        foreground='blue', cursor='hand2')
        # author_link.grid(row=0, column=1)
        # author_link.bind("<Button-1>", lambda e: self.open_github())
        
        # github_label = ttk.Label(author_frame, text=" | GitHub: github.com/Rajeshpaul1994", 
        #                         font=('Arial', 9), foreground='gray')
        # github_label.grid(row=0, column=2)
        
        # API URL
        ttk.Label(main_frame, text="API URL:").grid(row=3, column=0, sticky=tk.W, pady=5)
        self.url_entry = ttk.Entry(main_frame, width=60)
        self.url_entry.grid(row=3, column=1, pady=5, padx=(10, 0))
        self.url_entry.insert(0, "https://api.coingecko.com/api/v3/simple/price?ids=bitcoin,ethereum,tron,doge,ripple,bnb,cardano,stellar,sui,shib,link&vs_currencies=usd")
        
        # API Key
        ttk.Label(main_frame, text="API Key:").grid(row=4, column=0, sticky=tk.W, pady=5)
        self.api_key_entry = ttk.Entry(main_frame, width=60, show="*")
        self.api_key_entry.grid(row=4, column=1, pady=5, padx=(10, 0))
        
        # Duration (minutes)
        ttk.Label(main_frame, text="Duration (minutes):").grid(row=5, column=0, sticky=tk.W, pady=5)
        self.duration_entry = ttk.Entry(main_frame, width=20)
        self.duration_entry.grid(row=5, column=1, sticky=tk.W, pady=5, padx=(10, 0))
        self.duration_entry.insert(0, "5")
        
        # Time Gap (seconds)
        ttk.Label(main_frame, text="Time Gap (seconds):").grid(row=6, column=0, sticky=tk.W, pady=5)
        self.time_gap_entry = ttk.Entry(main_frame, width=20)
        self.time_gap_entry.grid(row=6, column=1, sticky=tk.W, pady=5, padx=(10, 0))
        self.time_gap_entry.insert(0, "30")
        
        # CSV File Name
        ttk.Label(main_frame, text="CSV File Name:").grid(row=7, column=0, sticky=tk.W, pady=5)
        self.csv_name_entry = ttk.Entry(main_frame, width=40)
        self.csv_name_entry.grid(row=7, column=1, sticky=tk.W, pady=5, padx=(10, 0))
        self.csv_name_entry.insert(0, "api_data.csv")
        
        # Buttons frame
        buttons_frame = ttk.Frame(main_frame)
        buttons_frame.grid(row=8, column=0, columnspan=2, pady=20)
        
        # Start/Stop button
        self.start_stop_btn = ttk.Button(buttons_frame, text="Start Polling", 
                                        command=self.toggle_polling)
        self.start_stop_btn.grid(row=0, column=0, padx=5)
        
        # Save File button (initially disabled)
        self.save_btn = ttk.Button(buttons_frame, text="Save to Downloads", 
                                  command=self.save_to_downloads, state="disabled")
        self.save_btn.grid(row=0, column=1, padx=5)
        
        # Status frame
        status_frame = ttk.LabelFrame(main_frame, text="Status", padding="10")
        status_frame.grid(row=9, column=0, columnspan=2, sticky=(tk.W, tk.E), pady=10)
        
        # Status label
        self.status_label = ttk.Label(status_frame, text="Ready to start polling")
        self.status_label.grid(row=0, column=0, sticky=tk.W)
        
        # Progress bar (initially hidden)
        self.progress = ttk.Progressbar(status_frame, mode='indeterminate')
        self.progress.grid(row=1, column=0, sticky=(tk.W, tk.E), pady=(10, 0))
        self.progress.grid_remove()  # Hide initially
        
        # Log text area
        log_frame = ttk.LabelFrame(main_frame, text="Log", padding="10")
        log_frame.grid(row=10, column=0, columnspan=2, sticky=(tk.W, tk.E, tk.N, tk.S), pady=10)
        
        # Scrollable text widget
        self.log_text = tk.Text(log_frame, height=8, width=70)
        scrollbar = ttk.Scrollbar(log_frame, orient="vertical", command=self.log_text.yview)
        self.log_text.configure(yscrollcommand=scrollbar.set)
        
        self.log_text.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))
        scrollbar.grid(row=0, column=1, sticky=(tk.N, tk.S))
        
        # Configure grid weights
        self.root.columnconfigure(0, weight=1)
        self.root.rowconfigure(0, weight=1)
        main_frame.columnconfigure(1, weight=1)
        main_frame.rowconfigure(10, weight=1)
        log_frame.columnconfigure(0, weight=1)
        log_frame.rowconfigure(0, weight=1)
        status_frame.columnconfigure(0, weight=1)
        
    def open_github(self):
        """Open GitHub profile in default browser"""
        import webbrowser
        webbrowser.open("https://github.com/Rajeshpaul1994")
        
    def log_message(self, message):
        """Add message to log with timestamp"""
        timestamp = datetime.now().strftime('%H:%M:%S')
        self.log_text.insert(tk.END, f"[{timestamp}] {message}\n")
        self.log_text.see(tk.END)
        self.root.update_idletasks()
        
    def validate_inputs(self):
        """Validate user inputs"""
        if not self.url_entry.get().strip():
            messagebox.showerror("Error", "Please enter an API URL")
            return False
            
        try:
            duration = float(self.duration_entry.get())
            if duration <= 0:
                raise ValueError
        except ValueError:
            messagebox.showerror("Error", "Please enter a valid duration (positive number)")
            return False
            
        try:
            time_gap = float(self.time_gap_entry.get())
            if time_gap <= 0:
                raise ValueError
        except ValueError:
            messagebox.showerror("Error", "Please enter a valid time gap (positive number)")
            return False
            
        if not self.csv_name_entry.get().strip():
            messagebox.showerror("Error", "Please enter a CSV file name")
            return False
            
        return True
        
    def create_file_if_not_exists(self, filename, dict_data):
        """Create CSV file with headers if it doesn't exist"""
        if not os.path.exists(filename):
            with open(filename, mode='w', newline='', encoding='utf-8') as file:
                writer = csv.writer(file)
                writer.writerow(dict_data.keys())
                
    def fetch_and_save_data(self):
        """Fetch data from API and save to CSV"""
        try:
            url = self.url_entry.get().strip()
            api_key = self.api_key_entry.get().strip()
            
            # Prepare headers
            headers = {}
            if api_key:
                headers['Authorization'] = f'Bearer {api_key}'
                headers['X-API-Key'] = api_key  # Common API key header
            
            # Make API request
            response = requests.get(url, headers=headers, timeout=30)
            response.raise_for_status()
            
            data = response.json()
            
            # Handle different API response structures
            if isinstance(data, dict):
                # For CoinGecko-style APIs
                if all(isinstance(v, dict) and 'usd' in v for v in data.values()):
                    # Transform CoinGecko format
                    flat_data = {key: val['usd'] for key, val in data.items()}
                else:
                    flat_data = data
            elif isinstance(data, list) and len(data) > 0:
                flat_data = data[0] if isinstance(data[0], dict) else {'data': str(data)}
            else:
                flat_data = {'response': str(data)}
            
            # Add timestamp
            utc_now = datetime.now(timezone.utc).strftime('%Y-%m-%d %H:%M:%S')
            flat_data['timestamp'] = utc_now
            
            # Create file if needed
            self.create_file_if_not_exists(self.csv_filepath, flat_data)
            
            # Append data to CSV
            with open(self.csv_filepath, mode='a', newline='', encoding='utf-8') as file:
                writer = csv.DictWriter(file, fieldnames=flat_data.keys())
                writer.writerow(flat_data)
            
            self.log_message(f"Data saved successfully ({len(flat_data)} fields)")
            return True
            
        except requests.exceptions.RequestException as e:
            self.log_message(f"API request failed: {str(e)}")
            return False
        except Exception as e:
            self.log_message(f"Error saving data: {str(e)}")
            return False
            
    def polling_worker(self):
        """Worker thread for polling data"""
        duration_minutes = float(self.duration_entry.get())
        time_gap_seconds = float(self.time_gap_entry.get())
        
        end_time = time.time() + (duration_minutes * 60)
        request_count = 0
        success_count = 0
        
        self.log_message(f"Starting polling for {duration_minutes} minutes with {time_gap_seconds}s intervals")
        
        while self.polling_active and time.time() < end_time:
            request_count += 1
            if self.fetch_and_save_data():
                success_count += 1
            
            # Update status
            remaining_time = max(0, end_time - time.time())
            self.status_label.config(text=f"Polling... {remaining_time:.0f}s remaining | "
                                        f"Requests: {request_count} | Success: {success_count}")
            
            # Wait for next request
            for _ in range(int(time_gap_seconds * 10)):  # Check every 0.1 seconds
                if not self.polling_active:
                    break
                time.sleep(0.1)
        
        # Polling finished
        self.polling_active = False
        self.root.after(0, self.polling_finished, request_count, success_count)
        
    def polling_finished(self, request_count, success_count):
        """Called when polling is finished"""
        self.start_stop_btn.config(text="Start Polling")
        self.progress.stop()
        self.progress.grid_remove()  # Hide progress bar
        self.save_btn.config(state="normal")
        
        if success_count > 0:
            self.status_label.config(text=f"Polling completed! {success_count}/{request_count} requests successful")
            self.log_message(f"Polling completed successfully. File saved: {self.csv_filepath}")
        else:
            self.status_label.config(text="Polling completed with errors")
            self.log_message("Polling completed but no data was saved")
        
    def toggle_polling(self):
        """Start or stop the polling process"""
        if not self.polling_active:
            # Start polling
            if not self.validate_inputs():
                return
                
            # Setup file path
            csv_name = self.csv_name_entry.get().strip()
            if not csv_name.endswith('.csv'):
                csv_name += '.csv'
            self.csv_filepath = os.path.join(os.getcwd(), csv_name)
            
            # Start polling
            self.polling_active = True
            self.start_stop_btn.config(text="Stop Polling")
            self.save_btn.config(state="disabled")
            self.progress.grid()  # Show progress bar
            self.progress.start()
            
            # Start worker thread
            self.polling_thread = threading.Thread(target=self.polling_worker, daemon=True)
            self.polling_thread.start()
            
        else:
            # Stop polling
            self.polling_active = False
            self.start_stop_btn.config(text="Start Polling")
            self.progress.stop()
            self.progress.grid_remove()  # Hide progress bar
            self.status_label.config(text="Stopping polling...")
            self.log_message("Polling stopped by user")
            
    def save_to_downloads(self):
        """Save the CSV file to Downloads folder"""
        if not self.csv_filepath or not os.path.exists(self.csv_filepath):
            messagebox.showerror("Error", "No data file found to save")
            return
            
        try:
            # Get Downloads folder
            downloads_folder = os.path.join(os.path.expanduser("~"), "Downloads")
            if not os.path.exists(downloads_folder):
                downloads_folder = filedialog.askdirectory(title="Select folder to save file")
                if not downloads_folder:
                    return
            
            # Copy file to Downloads
            filename = os.path.basename(self.csv_filepath)
            destination = os.path.join(downloads_folder, filename)
            
            # Handle duplicate filenames
            counter = 1
            base_name, ext = os.path.splitext(filename)
            while os.path.exists(destination):
                new_filename = f"{base_name}_{counter}{ext}"
                destination = os.path.join(downloads_folder, new_filename)
                counter += 1
            
            shutil.copy2(self.csv_filepath, destination)
            
            messagebox.showinfo("Success", f"File saved to:\n{destination}")
            self.log_message(f"File saved to Downloads: {os.path.basename(destination)}")
            
        except Exception as e:
            messagebox.showerror("Error", f"Failed to save file: {str(e)}")
            self.log_message(f"Error saving to Downloads: {str(e)}")

def main():
    root = tk.Tk()
    app = APIPollingGUI(root)
    root.mainloop()

if __name__ == "__main__":
    main()