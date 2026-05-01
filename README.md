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

Verify it worked:

```powershell
py -m cleanmap --help
```

You should see the help text. `py -m cleanmap` always works regardless of PATH. (The bare `cleanmap` command works too if your Python Scripts directory is on PATH, but `py -m cleanmap` is the safer default on Windows.)

> **macOS / Linux:** use `pip install git+https://github.com/DavidChen-006/cleanmap.git` (or `python3 -m pip install ...`).

## Update

To pull the latest version from GitHub:

```powershell
py -m pip install --upgrade --force-reinstall git+https://github.com/DavidChen-006/cleanmap.git
```

`--force-reinstall` is needed because pip may otherwise skip the install when the version number hasn't changed.

> **macOS / Linux:** `pip install --upgrade --force-reinstall git+https://github.com/DavidChen-006/cleanmap.git`

## Setup

Get a free Gemini API key: https://aistudio.google.com/apikey

Set it persistently (survives reboots, available in all future terminals):

```powershell
setx GEMINI_API_KEY "your-key-here"
```

**Two Windows gotchas:**
- Use a **space** between the name and value, **not `=`**. `setx GEMINI_API_KEY=value` fails with "Invalid syntax."
- `setx` only takes effect in *new* terminals — **close and reopen PowerShell** before using `cleanmap`.

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

Fastest way: type `py -m cleanmap ` (with a trailing space), then drag an image from File Explorer into the PowerShell window, hit Enter.

```powershell
py -m cleanmap "C:\Users\You\Downloads\photo.png"
# writes C:\Users\You\Downloads\photo.cleaned.png next to the input
```

**Wrap paths in double quotes** if they contain spaces (common in `C:\Users\...\Downloads\` filenames with spaces or `Screenshot 2026-04-22.png` style names).

### Flags

```powershell
py -m cleanmap "C:\path\to\photo.png" -o "C:\path\to\cleaned.png"    # custom output path
py -m cleanmap "C:\path\to\photo.png" -p "Remove only cars and people"  # override the cleaning prompt
py -m cleanmap --help                                                   # full help
```

> **Note:** `py -m cleanmap` is the Windows-safe invocation (always works). If your PATH is set up right, the bare `cleanmap` command works identically — same tool, either way.

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

**`setx` says `ERROR: Invalid syntax`** — you used `=` instead of a space. Correct form: `setx GEMINI_API_KEY "your-key"` (space, value in quotes, no `=`).

**`[WinError 2] ... websockets.exe.deleteme`** — a previous install got stuck. Fix: use a venv (`py -m venv .venv && .venv\Scripts\activate`) and reinstall. Venvs sidestep Windows system-Python permission issues.

**`'cleanmap' is not recognized`** — pip install succeeded but the shim isn't on your PATH. Quickest fix: run it as a Python module instead (no PATH needed):
>
> ```powershell
> py -m cleanmap "C:\path\to\photo.png"
> py -m cleanmap --help
> ```
>
> Works anywhere `py` works. You can alias it to `cleanmap` later or fix your PATH — but this unblocks you immediately.

**`GEMINI_API_KEY not set`** — you set it with `setx` but haven't opened a new terminal yet. `setx` writes to the permanent store, it doesn't touch your current session. Close and reopen PowerShell.

**Image returned but looks wrong / blurry / reframed** — Gemini occasionally ignores prompt constraints. Try a more specific `-p "..."` flag naming what to keep sharp, or run it again (the model is non-deterministic).

## How it works

```
CLI → load image bytes → Gemini 2.5 Flash Image (image + prompt) → save result
```
