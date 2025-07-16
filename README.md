# 🎧 Last.fm to CSV Exporter

A simple, no-login desktop tool that lets you export your Last.fm listening history (scrobbles) to a structured `.csv` file.  
Built with Python and Tkinter for an easy-to-use GUI.

---

## ✅ Features

- Export your **Last.fm scrobbles** to `.csv`
- Select a **date range** using a calendar widget
- Detect and mark **loved tracks**
- Consolidate play counts for repeated tracks
      <details>
      <summary>🤔 What does "Consolidate play counts for repeated tracks" mean?</summary>

    When a track is played multiple times during the selected date range,  
    the app groups all those plays into **one row** in the CSV.
    
    - ✅ `Playcount` shows **how many times** you played the same track
    - 🕒 `Played Time` reflects the **most recent play**
    - ❤️ `Loved` is set to 1 if **any** of the plays were loved

    This keeps your data **clean and compact**, without duplicates.
    
    </details>

- Choose **where to save the CSV file**
- Input via **username** or **profile URL**
- 

---

## 📷 Interface Overview

- Enter your Last.fm username or profile URL
- Select a time range (or choose **All time**)
- Browse and pick an output folder
- Preview the first 100 tracks before saving

---

## ⚙️ Running the App

### 🚀 Method 1: Use the `.exe` file

> 👉 [Download from Releases]([https://github.com/your-repo/releases](https://github.com/BadHumanX/LastFM-to-CSV/releases/tag/new))  
> No Python or installation required — just double-click and go.

### 🧪 Method 2: Run the Python script manually

#### 📦 Requirements

Make sure Python 3.9+ is installed. Then install these libraries:

```bash
pip install requests tkcalendar
```

The following libraries are built-in:
- `tkinter`
- `datetime`
- `csv`
- `os`  
*(No installation needed for these)*

#### ▶️ Launch the app

```bash
python gui_lastfm_to_csv.py
```

---

## 📂 CSV Output Format

The exported `.csv` file includes these columns:

| Column       | Description                      |
|--------------|----------------------------------|
| Played Time  | Timestamp of each scrobble       |
| Artist       | Artist name                      |
| Track Title  | Song name                        |
| Loved        | `1 = loved`, `0 = not loved`     |
| Playcount    | Number of times track was played |
