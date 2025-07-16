# 🎧 Last.fm to CSV Exporter

A simple, no-login desktop tool that lets you export your Last.fm listening history (scrobbles) to a structured CSV file.  

Built with Python and Tkinter for an easy-to-use GUI.

---

## ✅ Features

- Export your **Last.fm scrobbles** to `.csv`
- Select **date range** using a calendar widget
- Detects and marks **loved tracks**
- Consolidates play counts of repeated tracks
- Lets you choose **where to save the CSV**
- Supports input via **username** or **profile URL**

---

## 📷 Interface Preview

- Input your Last.fm username or profile URL
- Choose a time range (or select **All time**)
- Browse and select output folder
- Preview the first 100 tracks before saving

---

## ⚙️ Requirements (for Python CLI usage)

If running from source code:

```bash
pip install requests tkcalendar


Python 3.9 or higher

Internet connection (to fetch data from Last.fm)

🚀 How to Use
✅ Method 1: Run the .exe
Download the .exe from Releases

Double-click to run — no need to install Python or pip

✅ Method 2: Run the .py manually
If you'd rather run the Python script directly:

1. 📦 Requirements
Make sure you have Python 3.9+ installed.
Then, install these required libraries:

'''
bash
Copy
Edit
pip install requests tkcalendar
tkinter, datetime, csv, and os are built into Python and require no installation.

2. ▶️ Run the app
bash
Copy
Edit
python gui_lastfm_to_csv.py


📂 Output Example
Your generated CSV includes these columns:

Played Time

Artist

Track Title

Loved (1 = loved, 0 = not)

Playcount