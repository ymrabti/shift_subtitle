import tkinter as tk
from tkinter import filedialog, messagebox
import customtkinter as ctk
import re
from datetime import timedelta
from pathlib import Path
import os

# Set appearance mode and default color theme
ctk.set_appearance_mode("dark")
ctk.set_default_color_theme("blue")


class SubtitleShifterApp(ctk.CTk):
    def __init__(self):
        super().__init__()
        
        # Window configuration
        self.title("Subtitle Shifter")
        self.geometry("700x500")
        self.resizable(False, False)
        
        # Variables
        self.selected_file = None
        self.shift_var = tk.StringVar(value="0")
        
        # Configure grid
        self.grid_columnconfigure(0, weight=1)
        
        # Build UI
        self.create_widgets()
        
    def create_widgets(self):
        # Header
        header_frame = ctk.CTkFrame(self, fg_color="transparent")
        header_frame.grid(row=0, column=0, padx=30, pady=(30, 20), sticky="ew")
        
        title_label = ctk.CTkLabel(
            header_frame,
            text="⏱️ Subtitle Shifter",
            font=ctk.CTkFont(size=32, weight="bold")
        )
        title_label.pack()
        
        subtitle_label = ctk.CTkLabel(
            header_frame,
            text="Shift your subtitle timing effortlessly",
            font=ctk.CTkFont(size=14),
            text_color="gray"
        )
        subtitle_label.pack(pady=(5, 0))
        
        # Main content frame
        content_frame = ctk.CTkFrame(self)
        content_frame.grid(row=1, column=0, padx=30, pady=10, sticky="nsew")
        content_frame.grid_columnconfigure(0, weight=1)
        
        # File selection section
        file_label = ctk.CTkLabel(
            content_frame,
            text="Select SRT File",
            font=ctk.CTkFont(size=16, weight="bold"),
            anchor="w"
        )
        file_label.grid(row=0, column=0, padx=30, pady=(30, 10), sticky="w")
        
        file_frame = ctk.CTkFrame(content_frame, fg_color="transparent")
        file_frame.grid(row=1, column=0, padx=30, pady=(0, 20), sticky="ew")
        file_frame.grid_columnconfigure(0, weight=1)
        
        self.file_entry = ctk.CTkEntry(
            file_frame,
            placeholder_text="No file selected...",
            height=45,
            font=ctk.CTkFont(size=13),
            state="disabled"
        )
        self.file_entry.grid(row=0, column=0, sticky="ew", padx=(0, 10))
        
        browse_btn = ctk.CTkButton(
            file_frame,
            text="Browse",
            width=120,
            height=45,
            font=ctk.CTkFont(size=14, weight="bold"),
            command=self.browse_file
        )
        browse_btn.grid(row=0, column=1)
        
        # Shift amount section
        shift_label = ctk.CTkLabel(
            content_frame,
            text="Time Shift (milliseconds)",
            font=ctk.CTkFont(size=16, weight="bold"),
            anchor="w"
        )
        shift_label.grid(row=2, column=0, padx=30, pady=(10, 10), sticky="w")
        
        shift_frame = ctk.CTkFrame(content_frame, fg_color="transparent")
        shift_frame.grid(row=3, column=0, padx=30, pady=(0, 20), sticky="ew")
        
        self.shift_entry = ctk.CTkEntry(
            shift_frame,
            textvariable=self.shift_var,
            placeholder_text="Enter shift in ms (e.g., -1500 or 2000)",
            height=45,
            font=ctk.CTkFont(size=13)
        )
        self.shift_entry.grid(row=0, column=0, sticky="ew", pady=5)
        shift_frame.grid_columnconfigure(0, weight=1)
        
        hint_label = ctk.CTkLabel(
            shift_frame,
            text="💡 Use negative values to shift backwards, positive to shift forwards",
            font=ctk.CTkFont(size=12),
            text_color="gray",
            anchor="w"
        )
        hint_label.grid(row=1, column=0, sticky="w", pady=(5, 0))
        
        # Process button
        self.process_btn = ctk.CTkButton(
            content_frame,
            text="🚀 Shift Subtitles",
            height=55,
            font=ctk.CTkFont(size=16, weight="bold"),
            command=self.process_subtitles,
            fg_color="#1f6aa5",
            hover_color="#144870"
        )
        self.process_btn.grid(row=4, column=0, padx=30, pady=(10, 30), sticky="ew")
        
        # Status label
        self.status_label = ctk.CTkLabel(
            self,
            text="",
            font=ctk.CTkFont(size=12),
            text_color="gray"
        )
        self.status_label.grid(row=2, column=0, padx=30, pady=(0, 20))
        
    def browse_file(self):
        file_path = filedialog.askopenfilename(
            title="Select SRT File",
            filetypes=[("SRT files", "*.srt"), ("All files", "*.*")]
        )
        
        if file_path:
            self.selected_file = file_path
            self.file_entry.configure(state="normal")
            self.file_entry.delete(0, tk.END)
            self.file_entry.insert(0, Path(file_path).name)
            self.file_entry.configure(state="disabled")
            self.status_label.configure(text=f"📁 File: {file_path}", text_color="gray")
    
    def parse_time(self, time_str):
        """Convert SRT time string 'HH:MM:SS,mmm' to timedelta."""
        hours, minutes, seconds = time_str.split(':')
        seconds, milliseconds = seconds.split(',')
        return timedelta(
            hours=int(hours),
            minutes=int(minutes),
            seconds=int(seconds),
            milliseconds=int(milliseconds)
        )
    
    def format_time(self, td):
        """Convert timedelta back to SRT time string."""
        total_seconds = int(td.total_seconds())
        millis = int(td.microseconds / 1000)
        hours = total_seconds // 3600
        minutes = (total_seconds % 3600) // 60
        seconds = total_seconds % 60
        return f"{hours:02}:{minutes:02}:{seconds:02},{millis:03}"
    
    def shift_srt(self, input_path, output_path, shift_ms):
        """Shift subtitle times by given milliseconds."""
        shift = timedelta(milliseconds=shift_ms)
        time_pattern = re.compile(r"(\d{2}:\d{2}:\d{2},\d{3}) --> (\d{2}:\d{2}:\d{2},\d{3})")
        
        with open(input_path, 'r', encoding='utf-8') as infile, \
             open(output_path, 'w', encoding='utf-8') as outfile:
            
            for line in infile:
                match = time_pattern.match(line)
                if match:
                    start_time = self.parse_time(match.group(1)) + shift
                    end_time = self.parse_time(match.group(2)) + shift
                    
                    # prevent negative times
                    if start_time.total_seconds() < 0:
                        start_time = timedelta(0)
                    if end_time.total_seconds() < 0:
                        end_time = timedelta(0)
                    
                    outfile.write(f"{self.format_time(start_time)} --> {self.format_time(end_time)}\n")
                else:
                    outfile.write(line)
    
    def process_subtitles(self):
        # Validate file selection
        if not self.selected_file:
            messagebox.showerror("Error", "Please select an SRT file first!")
            return
        
        # Validate shift value
        try:
            shift_ms = int(self.shift_var.get())
        except ValueError:
            messagebox.showerror("Error", "Please enter a valid number for shift amount!")
            return
        
        # Generate output filename with suffix
        input_path = Path(self.selected_file)
        output_path = input_path.parent / f"{input_path.stem}_shifted{input_path.suffix}"
        
        # Process the file
        try:
            self.status_label.configure(text="⏳ Processing...", text_color="orange")
            self.update()
            
            self.shift_srt(str(input_path), str(output_path), shift_ms)
            
            self.status_label.configure(
                text=f"✅ Success! Saved to: {output_path.name}",
                text_color="green"
            )
            
            messagebox.showinfo(
                "Success",
                f"Subtitles shifted by {shift_ms} ms\n\nSaved to:\n{output_path}"
            )
            
        except Exception as e:
            self.status_label.configure(text="❌ Error occurred", text_color="red")
            messagebox.showerror("Error", f"An error occurred:\n{str(e)}")


def main():
    app = SubtitleShifterApp()
    app.mainloop()


if __name__ == "__main__":
    main()
