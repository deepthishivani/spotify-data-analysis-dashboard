# 🎯 VS Code Setup Guide - Spotify Data Analysis

## Quick Start (3 minutes)

### 1. Unzip & Open
```bash
# Unzip the file
unzip spotify-data-analysis-dashboard.zip

# Open in VS Code
cd spotify_project
code .
```

Or **simpler**: Open VS Code → File → Open Folder → Select `spotify_project`

---

## 2. Open Workspace (Recommended)

When you first open the folder, you'll see `spotify-dashboard.code-workspace` file.

**Click it or run:**
```bash
code spotify-dashboard.code-workspace
```

This loads all VS Code settings, debug configs, and tasks automatically.

---

## 3. Install Python Extension

VS Code will prompt you. If not:

1. Click Extensions icon (left sidebar) or `Cmd+Shift+X`
2. Search "Python"
3. Install **Python** by Microsoft (the one with 70M+ downloads)

**Also install (recommended):**
- Pylance (auto-suggests with Python extension)
- Pandas extensions if you want

---

## 4. Create Virtual Environment

**Terminal in VS Code:**
```bash
# Mac/Linux
python3 -m venv venv
source venv/bin/activate

# Windows
python -m venv venv
venv\Scripts\activate
```

Or use VS Code's built-in: `Cmd+Shift+P` → "Python: Create Environment" → Select venv

---

## 5. Install Dependencies

**In VS Code terminal (venv activated):**
```bash
pip install -r requirements.txt
```

Or use the Task: `Cmd+Shift+P` → "Run Build Task" → "Install Dependencies"

---

## 6. Download Kaggle Dataset

1. Go to https://www.kaggle.com/datasets/yamaerenay/spotify-dataset-19212020-600k-tracks
2. Download CSV
3. Place in `spotify_project` folder as `spotify_tracks.csv`

Folder should look like:
```
spotify_project/
├── spotify_analysis.py
├── spotify_visualizations.py
├── spotify_tracks.csv          ← Add this
├── requirements.txt
└── ... other files
```

---

## 7. Run Analysis

### Option A: Use VS Code Debug (Easiest)
1. Open `spotify_analysis.py`
2. Click **Run** button (top right) or press `F5`
3. Select "Python: Run Analysis"
4. Watch output in Terminal

### Option B: Use Terminal
```bash
python spotify_analysis.py
```

### Option C: Use Tasks
1. `Cmd+Shift+P` → "Run Task"
2. Select "Run Analysis"

---

## 8. Generate Visualizations

Same process with `spotify_visualizations.py`:

**VS Code:** Open file → Click Run → Select "Python: Run Visualizations"

**Terminal:** `python spotify_visualizations.py`

Charts appear in `visualizations/` folder

---

## 🎮 VS Code Keyboard Shortcuts (Gold Standard)

| Action | Shortcut |
|--------|----------|
| Open Command Palette | `Cmd+Shift+P` |
| Run/Debug | `F5` |
| Run Terminal | `Ctrl+`` |
| Open File | `Cmd+P` |
| Find in File | `Cmd+F` |
| Find & Replace | `Cmd+H` |
| Split Editor | `Cmd+\` |
| Go to Line | `Ctrl+G` |
| Format Code | `Shift+Option+F` |
| Rename Variable | `F2` |
| Quick Fix | `Cmd+.` |

---

## 💡 Pro VS Code Tips

### 1. **Intellisense (Auto-complete)**
Start typing `self.df` → VS Code suggests `.groupby()`, `.agg()`, etc.
- Python extension reads your code
- Understands Pandas methods

### 2. **Debugger Breakpoints**
Click left of line number to set breakpoint:
```python
def popularity_analysis(self):
    popularity = self.df['popularity']  ← Click here to set breakpoint
```

Then press `F5` to debug step-by-step.

### 3. **Inline Variable Inspection**
Hover over variable to see value:
```python
correlations = {}  ← Hover → shows type: dict
```

### 4. **Docstring Hover**
Hover over function to see docstring:
```python
self.df.groupby()  ← Hover → shows pandas documentation
```

### 5. **Run Selection**
Select code → `Cmd+Shift+P` → "Run Selection in Python Terminal"

Perfect for testing code snippets.

### 6. **Multiple Terminals**
Click `+` in terminal to open second terminal
- One for running analysis
- One for Git commands

### 7. **Source Control (Git)**
Click Source Control icon (left) → Commit changes without terminal
- Stage files
- Write commit message
- Push to GitHub

---

## 📂 File Structure in VS Code

After setup, your folder tree looks like:
```
spotify_project (workspace)
├── .gitignore
├── .vscode/
│   ├── launch.json (debug config)
│   └── tasks.json (task definitions)
├── config.py
├── spotify_analysis.py
├── spotify_visualizations.py
├── spotify_tracks.csv (you add this)
├── spotify_tracks_analyzed.csv (created after running)
├── visualizations/ (created after running)
│   ├── 01_popularity_distribution.png
│   ├── 02_temporal_trends.png
│   └── ... (6 more charts)
├── requirements.txt
├── README.md
├── QUICKSTART.md
├── TEACHING_GUIDE.md
└── spotify-dashboard.code-workspace
```

---

## 🐛 Debugging in VS Code

### Debug Mode (Best for Learning)

1. Open `spotify_analysis.py`
2. Set breakpoint at line you want to inspect:
   ```python
   def load_data(self):
       self.df = pd.read_csv(self.data_path)  ← Click left margin
   ```
3. Press `F5` → Select "Python: Run Analysis"
4. Execution stops at breakpoint
5. Use Debug Console (bottom) to inspect:
   ```
   > self.df.shape
   (10000, 18)
   > self.df.columns
   ['name', 'artists', 'popularity', ...]
   ```
6. Step through code:
   - `F10` = Step over (next line)
   - `F11` = Step into (enter function)
   - `Shift+F11` = Step out (exit function)
   - `F5` = Continue to next breakpoint

### Print Debugging
```python
print(f"DEBUG: popularity type = {type(popularity)}")
print(f"DEBUG: df shape = {self.df.shape}")
```

Output appears in Terminal.

---

## 🚀 Workflow Recommendation

### Daily Workflow:

1. **Open Workspace**
   ```bash
   cd ~/spotify_project
   code spotify-dashboard.code-workspace
   ```

2. **Activate Terminal** (Ctrl+`)
   ```bash
   source venv/bin/activate
   ```

3. **Edit Code** (Main editor)
   - Modify `spotify_analysis.py`
   - Intellisense helps with Pandas methods

4. **Test Changes** (Run button or F5)
   - Execution stops on errors
   - Read error message in terminal

5. **Debug** (Breakpoints if needed)
   - Set breakpoint
   - Run with debugger
   - Inspect variables

6. **Git Commit** (Source Control icon)
   - Stage changes
   - Write message
   - Commit

---

## ✅ Checklist Before Running

- [ ] VS Code open with workspace
- [ ] Python extension installed
- [ ] Virtual environment created (`venv` folder exists)
- [ ] Virtual environment activated (terminal shows `(venv)` prefix)
- [ ] Dependencies installed (`pip install -r requirements.txt`)
- [ ] `spotify_tracks.csv` in project folder
- [ ] `visualizations/` folder will auto-create

---

## 📊 After Running Analysis

**Console Output:**
```
SPOTIFY DATA ANALYSIS DASHBOARD

✓ Dataset loaded: 10000 tracks, 18 features

============================================================
BASIC STATISTICS
============================================================
...
```

**Files Created:**
- `spotify_tracks_analyzed.csv` → Enriched dataset with new columns
- `visualizations/` folder → 8 PNG charts at 300 DPI

**View Charts:**
Open `visualizations/` folder in VS Code file explorer. Right-click any PNG → "Open with Preview"

---

## 🎓 Interview Prep in VS Code

1. **Understand Every Line:**
   - Click on function name → `F12` jumps to definition
   - Hover for docstrings
   - Read inline comments

2. **Modify Code Confidently:**
   - Change a parameter → See what breaks
   - Edit a function → Intellisense shows what's available
   - Run tests → Debug output shows what happened

3. **Explain Your Code:**
   - With file open, point and explain each section
   - Walk through logic line-by-line
   - Use debugger to show variable values

---

## Troubleshooting

### "Python interpreter not found"
1. `Cmd+Shift+P` → "Python: Select Interpreter"
2. Choose `./venv/bin/python`

### "Module 'pandas' not found"
1. Check venv is activated: terminal should show `(venv)` prefix
2. Reinstall: `pip install -r requirements.txt`

### "Breakpoint not working"
1. Make sure you're running with debugger (`F5`), not just executing
2. Breakpoint must be in executable code, not comments

### "Can't see visualizations"
1. Check `visualizations/` folder exists
2. Right-click PNG → "Open with Preview"
3. Or open in separate image viewer

---

## Extensions Worth Adding

**For this project specifically:**
- **Python** (Microsoft) - Language support
- **Pylance** (Microsoft) - Smart intellisense
- **Rainbow CSV** - Better CSV viewing
- **Prettier** - Code formatting
- **Git Graph** - Visualize Git history

**Optional (for future projects):**
- Jupyter (for notebooks)
- Streamlit (for dashboards)
- REST Client (for APIs)

---

## Final Tips

1. **Save frequently** (`Cmd+S`)
2. **Use integrated terminal** (Ctrl+`) — stays in project folder
3. **Learn keyboard shortcuts** — makes you 2x faster
4. **Use debugger early** — saves hours of confusion
5. **Commit to GitHub often** — shows progress

---

**Ready?** 

1. Unzip the file
2. Open folder in VS Code
3. Run `source venv/bin/activate`
4. Run `pip install -r requirements.txt`
5. Add `spotify_tracks.csv`
6. Press `F5` to run analysis

Let me know if you get stuck! 🚀
