# !/usr/bin/env python3
"""
file_organizer_v2.py

Features:
- Categorizes files into folders (Images, Videos, Documents, Audio, Archives, Code, Others)
- Uses tkinter.filedialog for a GUI folder picker (falls back to console input)
- Handles duplicate filenames by appending a counter (file_copy_1.txt)
- Removes empty folders after organizing
- Writes a detailed log file (organizer.log) describing moves and errors
- Optional console progress bar using tqdm if available
- Safe path handling with os.path.join
- Cross-platform friendly

Usage:
- Run normally: python file_organizer_v2.py
- Select a folder in the GUI dialog, or press Cancel to enter a path manually in the console.
"""
import os
import shutil
import logging
from datetime import datetime

# Try to import GUI folder picker
try:
    import tkinter as tk
    from tkinter import filedialog, messagebox
    TK_AVAILABLE = True
except Exception:
    TK_AVAILABLE = False

# Optional progress bar
try:
    from tqdm import tqdm
    TQDM_AVAILABLE = True
except Exception:
    TQDM_AVAILABLE = False

CATEGORIES = {
    "Images": [".jpg", ".jpeg", ".png", ".gif", ".bmp", ".webp"],
    "Videos": [".mp4", ".mkv", ".flv", ".mov", ".avi"],
    "Documents": [".pdf", ".docx", ".doc", ".txt", ".pptx", ".xlsx"],
    "Audio": [".mp3", ".wav", ".aac", ".ogg"],
    "Archives": [".zip", ".rar", ".tar", ".gz"],
    "Code": [".py", ".cpp", ".java", ".html", ".css", ".js"]
}

LOG_FILENAME = "organizer.log"

def setup_logger(log_path):
    logger = logging.getLogger("file_organizer")
    logger.setLevel(logging.DEBUG)
    formatter = logging.Formatter("%(asctime)s - %(levelname)s - %(message)s")

    fh = logging.FileHandler(log_path, encoding="utf-8")
    fh.setLevel(logging.DEBUG)
    fh.setFormatter(formatter)
    logger.addHandler(fh)

    # also log to console
    ch = logging.StreamHandler()
    ch.setLevel(logging.INFO)
    ch.setFormatter(formatter)
    logger.addHandler(ch)

    return logger

def categorize_file(filename):
    ext = os.path.splitext(filename)[1].lower()
    for category, extensions in CATEGORIES.items():
        if ext in extensions:
            return category
    return "Others"

def increment_filename_if_exists(dest_folder, filename):
    base, ext = os.path.splitext(filename)
    candidate = filename
    counter = 1
    while os.path.exists(os.path.join(dest_folder, candidate)):
        candidate = f"{base}_copy_{counter}{ext}"
        counter += 1
    return candidate

def remove_empty_folders(path, logger=None):
    removed = []
    for entry in os.listdir(path):
        entry_path = os.path.join(path, entry)
        if os.path.isdir(entry_path):
            try:
                if not os.listdir(entry_path):
                    os.rmdir(entry_path)
                    removed.append(entry_path)
                    if logger:
                        logger.info(f"Removed empty folder: {entry_path}")
            except Exception as e:
                if logger:
                    logger.warning(f"Could not remove folder {entry_path}: {e}")
    return removed

def organize_files(path, logger=None):
    if logger:
        logger.info(f"Starting organization in: {path}")
    files = os.listdir(path)
    total = len(files)
    processed = 0

    iterable = files
    if TQDM_AVAILABLE:
        iterable = tqdm(files, desc="Organizing files", unit="file")

    for file in iterable:
        file_path = os.path.join(path, file)
        # skip directories
        if os.path.isdir(file_path):
            continue

        try:
            category = categorize_file(file)
            category_folder = os.path.join(path, category)
            if not os.path.exists(category_folder):
                os.makedirs(category_folder, exist_ok=True)

            # handle duplicates
            dest_name = increment_filename_if_exists(category_folder, file)
            destination = os.path.join(category_folder, dest_name)

            shutil.move(file_path, destination)
            processed += 1
            if logger:
                logger.info(f"Moved: {file_path} -> {destination}")
        except Exception as e:
            if logger:
                logger.exception(f"Error moving {file_path}: {e}")
    # cleanup empty folders
    removed = remove_empty_folders(path, logger=logger)
    if logger:
        logger.info(f"Finished. Processed {processed} files. Removed {len(removed)} empty folders.")
    return processed, removed

def pick_folder_gui():
    root = tk.Tk()
    root.withdraw()
    root.attributes("-topmost", True)
    folder = filedialog.askdirectory(title="Select folder to organize")
    root.destroy()
    return folder

def main():
    # logger in script directory
    script_dir = os.path.dirname(os.path.abspath(__file__))
    log_path = os.path.join(script_dir, LOG_FILENAME)
    logger = setup_logger(log_path)
    logger.info("---- New run ----")

    folder = None
    if TK_AVAILABLE:
        try:
            folder = pick_folder_gui()
            if not folder:
                # user canceled GUI - ask in console
                folder = input("No folder selected. Enter folder path manually: ").strip()
        except Exception as e:
            logger.warning(f"GUI folder picker failed: {e}")
            folder = input("Enter folder path: ").strip()
    else:
        folder = input("Enter folder path: ").strip()

    if not folder:
        logger.error("No folder provided. Exiting.")
        return

    if not os.path.exists(folder):
        logger.error(f"Invalid path: {folder}")
        print("❌ Invalid path! Please check again.")
        return

    # Confirm with user (console confirmation)
    print(f"Organize files in: {folder}")
    confirm = input("Proceed with organizing? (y/n): ").lower().strip()
    if confirm != 'y':
        logger.info("Operation cancelled by user.")
        print("❌ Operation cancelled.")
        return

    processed, removed = organize_files(folder, logger=logger)
    print(f"\n✅ Done! Processed {processed} files. Removed {len(removed)} empty folders.")
    print(f"Log saved to: {log_path}")

if __name__ == "__main__":
    main()
