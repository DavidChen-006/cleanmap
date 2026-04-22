# cleanmap

CLI tool for cleaning images — strips clutter (cars, people, trees, signs) and returns the main subject. Powered by Gemini 2.5 Flash Image.

> Docs are written for **Windows (PowerShell)**. macOS/Linux notes included where syntax differs.

## Install

Open PowerShell and run:

```powershell
py -m pip install git+https://github.com/DavidChen-006/cleanmap.git
```

That's it. pip fetches the repo, installs dependencies, and puts `cleanmap` on your PATH.

Requires Python 3.10+. If you don't have Python, install it from https://python.org — **tick "Add Python to PATH"** on the first installer screen.

> **macOS / Linux:** use `pip install git+https://github.com/DavidChen-006/cleanmap.git` (or `python3 -m pip install ...`).

## Setup

Get a free Gemini API key: https://aistudio.google.com/apikey

Set it persistently (survives reboots, available in all future terminals):

```powershell
setx GEMINI_API_KEY "your-key-here"
```

**Then close and reopen PowerShell** — `setx` only takes effect in *new* terminals, not the one you ran it in.

To verify it's set, open a new PowerShell and run:

```powershell
echo $env:GEMINI_API_KEY
```

### Session-only alternative

If you only want the key for the current terminal:

```powershell
$env:GEMINI_API_KEY = "your-key-here"
```

Gone when you close the window.

> **macOS / Linux:** `export GEMINI_API_KEY=your-key-here` (session-only). Add the line to `~/.zshrc` or `~/.bashrc` to make it permanent.

## Usage

```powershell
cleanmap photo.png
# writes photo.cleaned.png next to the input
```

Drag-and-drop works: type `cleanmap `, then drag an image from File Explorer into the terminal, hit Enter.

### Flags

```powershell
cleanmap photo.png -o cleaned.png                     # custom output path
cleanmap photo.png -p "Remove only cars and people"   # override the cleaning prompt
cleanmap --help                                       # full help
```

## Dev install (if you want to modify the code)

```powershell
git clone https://github.com/DavidChen-006/cleanmap.git
cd cleanmap
py -m venv .venv
.venv\Scripts\activate
py -m pip install -e .
```

Edit `.py` files — changes are live on next `cleanmap` run thanks to `-e`.

> **macOS / Linux:** use `python3 -m venv .venv && source .venv/bin/activate && pip install -e .`.

## Troubleshooting

**`'pip' is not recognized`** — use `py -m pip ...` instead. Same result, doesn't require `pip.exe` to be on PATH.

**`'export' is not recognized`** — that's Unix syntax. On Windows use `setx` (persistent) or `$env:VAR = "..."` (session).

**`[WinError 2] ... websockets.exe.deleteme`** — a previous install got stuck. Fix: use a venv (`py -m venv .venv && .venv\Scripts\activate`) and reinstall. Venvs sidestep Windows system-Python permission issues.

**`cleanmap: The term 'cleanmap' is not recognized`** — pip install succeeded but the shim isn't on your PATH. Either activate the venv you installed into, or close/reopen PowerShell.

## How it works

```
CLI → load image bytes → Gemini 2.5 Flash Image (image + prompt) → save result
```
