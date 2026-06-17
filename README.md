# 📁 Folder Tree

Navigate any folder — files and all — as a fast, searchable tree. Built for people who find jumping between OneDrive folders disorienting.

**[Open the app →](https://tobiko-dev.github.io/folder-tree)**

---

## What it does

Paste a folder path, run one command, and your entire directory structure becomes an interactive tree you can explore, search, and click through — without ever leaving the browser.

---

## Quick start (2 minutes)

### 1. Open the app

Go to **[tobiko-dev.github.io/folder-tree](https://tobiko-dev.github.io/folder-tree)** in **Chrome or Edge.**

---

### 2. Get your folder path

Open the folder you want to explore in **File Explorer**. Then click the address bar at the top — it shows the full path.

```
Click here ↓
┌─────────────────────────────────────────────────────────┐
│  C:\Users\YourName\OneDrive - Company Name              │
└─────────────────────────────────────────────────────────┘
```

Press **Ctrl+A** to select it, then **Ctrl+C** to copy. Paste it into the app.

> The path must start with a drive letter like `C:\` — if you only see a folder name, click directly on the address bar text to reveal the full path.

---

### 3. Run the command

The app generates a command for you the moment you paste your path:

```
tree /f /a "C:\Users\YourName\OneDrive - Company Name" | clip
```

- Open **Command Prompt** (search `cmd` in the Start menu)
- Paste the command and press **Enter**
- The output copies to your clipboard automatically — the `| clip` part handles this, no manual selecting needed

---

### 4. View your tree

Back in the app, click **Step 3 — Paste & view tree**.

If your browser blocks clipboard access, the button changes to say **"Press Ctrl+V anywhere on this page"** — just press Ctrl+V and the tree loads.

---

## Navigating the tree

Once your tree is loaded:

| What you want to do | How |
|---|---|
| Open / close a folder | Click it |
| Open everything at once | **Expand all** in the toolbar |
| Collapse back to top level | **Collapse all** in the toolbar |
| Find a file or folder | Type in the **Search** box — matches highlight and parent folders open automatically |
| Clear the search | Click **✕** next to the search box |
| Go back to load a different folder | Click **← Back** |

---

## Opening files and folders with Ctrl+click

By default, Ctrl+clicking a file or folder copies its full path to your clipboard. To actually *open* things — folders in Explorer, files in their default app (Excel, Notepad, VS Code, etc.) — you need the helper script.

### Setup (one time)

1. Download **`helper.py`** and **`start_helper.bat`** from this repository and put them in the same folder as `index.html`
2. Double-click **`start_helper.bat`** — a Command Prompt window opens and shows:
   ```
   Listening on http://localhost:7432
   Keep this window open while browsing
   ```
3. Keep that window open whenever you use Folder Tree

### Using Ctrl+click

With the helper running:

- **Ctrl+click a folder** → opens it in Windows Explorer
- **Ctrl+click a file** → opens it with your default app (same as double-clicking in Explorer)

Without the helper running, Ctrl+click still works — it just copies the path to your clipboard instead, with a message telling you the path.

> **Requirement:** Python must be installed. Check by opening Command Prompt and typing `python --version`. If it's not installed, download it from [python.org](https://python.org).

---

## Troubleshooting

### "Can't open this folder — contains system files"

This appears when clicking Browse and navigating to Documents, Downloads, Desktop, or other protected Windows folders. Chrome and Edge block direct access to those locations.

**Fix:** Skip the Browse button. Use the path input + command approach described in the Quick Start — it works for every folder without restrictions.

---

### "Clipboard access blocked"

This happens when the app is opened as a local file (`file:///`) rather than via a web server. The button text changes to guide you:

> *"Now press Ctrl+V anywhere on this page"*

Just press **Ctrl+V** — the tree loads immediately. No extra steps needed.

---

### Files aren't showing, only folders

The command uses `/f` to include files. If you're not seeing files, make sure you're running the exact command the app generates:

```
tree /f /a "C:\your\path" | clip
```

Not just `tree /a` (which shows folders only).

---

### Ctrl+click does nothing or just expands the folder

Make sure you entered your folder path in the input field **before** running the command. The app uses that path to reconstruct where every file and folder lives. Without it, paths can't be calculated and Ctrl+click falls back to showing a message.

---

### The command says "Invalid path" or "No subfolders exist"

The path in the command doesn't point to a real folder. Common causes:

- You pasted a folder **name** instead of the full **path** — the path must start with `C:\` (or another drive letter)
- The folder is on a network drive that uses a different path format — try navigating to it in File Explorer and copying the address bar

---

## Hosting on GitHub Pages

To share the app with your team via a link:

1. Push `index.html`, `helper.py`, and `README.md` to a GitHub repository
2. Go to **Settings → Pages → Source: Deploy from a branch → main → / (root) → Save**
3. The app goes live at `https://your-username.github.io/your-repo-name` within a minute

Anyone on your team can use the web app. They'll each need to download and run `helper.py` locally if they want Ctrl+click to open files.

---

## Browser support

| Browser | Works |
|---|---|
| Chrome 86+ | ✅ |
| Edge 86+ | ✅ |
| Firefox | ❌ |
| Safari | ❌ |

Firefox and Safari don't support the File System Access API or the clipboard features this app depends on.

---

## How it works (for the curious)

The app is a single `index.html` file with no framework, no build step, and no external dependencies.

When you run `tree /f /a "path" | clip`, Windows walks your directory and writes a text-based tree to your clipboard. The `/f` flag includes files, `/a` uses plain characters that are easy to parse, and `| clip` pipes the output straight to your clipboard so you don't have to copy it manually.

The app parses that text into a data structure, reconstructs the full path for every file and folder using the path you typed, and renders the interactive tree entirely in your browser. Nothing is sent anywhere.

The `helper.py` script runs a small local server on `localhost:7432`. When you Ctrl+click, the browser calls it, and it uses Python's `os.startfile()` and `subprocess` to open things natively — the same mechanism as double-clicking in Explorer.
