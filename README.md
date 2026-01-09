# Subtitle Shifter

A modern desktop application to shift subtitle timing in SRT files.

## 📦 Executable File

The standalone executable is located in the `dist` folder:
- **File**: `SubtitleShifter.exe`
- **Location**: `dist/SubtitleShifter.exe`

## 🚀 How to Use

### Option 1: Run the Executable (No Python Required)
1. Navigate to the `dist` folder
2. Double-click `SubtitleShifter.exe`
3. The application will open with a modern dark-themed interface

### Option 2: Run from Python Source
```bash
python shift_srt_ui.py
```

## 💡 Features

- **Browse & Select**: Choose any SRT subtitle file from your computer
- **Time Shift**: Enter positive or negative milliseconds to shift subtitles
- **Auto-Save**: Output is automatically saved with "_shifted" suffix in the same folder
- **Modern UI**: Clean, dark-themed interface with intuitive controls
- **Error Handling**: User-friendly error messages and validation

## 📝 Usage Instructions

1. **Click "Browse"** to select your SRT subtitle file
2. **Enter shift amount** in milliseconds:
   - Use **negative values** (e.g., `-1500`) to shift subtitles backward
   - Use **positive values** (e.g., `2000`) to shift subtitles forward
3. **Click "🚀 Shift Subtitles"**
4. Find your new subtitle file in the same folder with the `_shifted` suffix

### Example
- Input file: `movie.srt`
- Shift: `-1500` ms (1.5 seconds backward)
- Output file: `movie_shifted.srt` (saved in the same folder as input)

## 🛠️ Building from Source

If you want to rebuild the executable:

```bash
# Install dependencies
pip install -r requirements.txt

# Build executable
pyinstaller --onefile --windowed --name "SubtitleShifter" shift_srt_ui.py
```

The executable will be created in the `dist` folder.

## 📋 Requirements (for running from source)

- Python 3.7+
- customtkinter
- packaging

## 📄 Original CLI Script

The original command-line version is still available in `shift_srt.py`.

Usage:
```bash
python shift_srt.py input.srt output.srt shift_ms
```

Example:
```bash
python shift_srt.py movie.srt movie_shifted.srt -1500
```
