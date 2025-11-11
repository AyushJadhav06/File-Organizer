# File Organizer (file_organizer_v2)

A robust Python script to organize files in a folder into categorized subfolders (Images, Videos, Documents, Audio, Archives, Code, Others).

## Features
- GUI folder picker using `tkinter.filedialog` (falls back to console input if GUI not available)
- Handles duplicate filenames by appending `_copy_n` suffix
- Removes empty folders after organizing
- Writes a log file `organizer.log` in the script directory with detailed info
- Optional progress bar support if `tqdm` is installed

## Requirements
- Python 3.7+
- Optional packages:
  - `tqdm` (progress bar) — `pip install tqdm`

`tkinter` usually comes bundled with standard Python installers. If you don't have it, install it for your OS.

## Usage
1. Save/Place `file_organizer_v2.py` somewhere (e.g., Desktop).
2. Open a terminal and run:
```bash
python file_organizer_v2.py
```
3. A folder selection dialog will appear. Choose the folder to organize.
4. Confirm operation in the console.
5. After the run, check `organizer.log` next to the script for full details.

## Convert to .exe (Windows)
Install PyInstaller if you don't have it:
```bash
pip install pyinstaller
```
Then create a single-file executable:
```bash
pyinstaller --onefile file_organizer_v2.py
```
The `.exe` will be inside the `dist/` folder. Test it on a machine with the same architecture.

## Upload to GitHub
1. Create a new repository on GitHub.
2. Initialize git locally:
```bash
git init
git add file_organizer_v2.py README.md
git commit -m "Add file organizer v2"
git branch -M main
git remote add origin https://github.com/yourusername/your-repo.git
git push -u origin main
```
(Replace `yourusername/your-repo` with your repository URL.)

## Notes & Safety
- The script **moves** files (not copies) — be careful with important data. Try it on a test folder first.
- The log file records every move and any errors encountered.

## License
MIT
