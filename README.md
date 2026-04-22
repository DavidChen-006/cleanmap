# cleanmap

CLI tool for cleaning images — strips clutter (cars, people, trees, signs) and returns the main subject. Powered by Gemini 2.5 Flash Image.

## Install

Direct from GitHub (recommended for teammates):

```
pip install git+https://github.com/DavidChen-006/cleanmap.git
```

That's it. pip fetches the repo, installs dependencies, and puts `cleanmap` on your PATH.

Requires Python 3.10+.

## Setup

Get a free Gemini API key: https://aistudio.google.com/apikey

Export it (or put it in a `.env` file in your working directory):

```
export GEMINI_API_KEY=your-key-here
```

> **Note:** `export GEMINI_API_KEY=...` only lasts for that terminal window. Close the terminal and it's gone — open a new one and you'll have to export again.
>
> To make it permanent, add the line to `~/.zshrc` (or `~/.bashrc`), or use a `.env` file in your project directory (`cleanmap` auto-loads it).

## Usage

```
cleanmap photo.png
# writes photo.cleaned.png next to the input
```

Drag-and-drop works: type `cleanmap `, then drag an image from Finder into the terminal, hit Enter.

### Flags

```
cleanmap photo.png -o cleaned.png                  # custom output path
cleanmap photo.png -p "Remove only cars and people" # override the cleaning prompt
cleanmap --help                                     # full help
```

## Dev install (if you want to modify the code)

```
git clone https://github.com/DavidChen-006/cleanmap.git
cd cleanmap
python3 -m venv .venv && source .venv/bin/activate
pip install -e .
```

Edit `.py` files — changes are live on next `cleanmap` run thanks to `-e`.

## How it works

```
CLI → load image bytes → Gemini 2.5 Flash Image (image + prompt) → save result
```
