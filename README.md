# cleanmap

CLI tool for cleaning images — strips clutter (cars, people, trees) and returns the main subject. Powered by Gemini 2.5 Flash Image.

## Install

```
pip install -e .
```

## Setup

Get a Gemini API key: https://aistudio.google.com/apikey

```
cp .env.example .env
# edit .env and set GEMINI_API_KEY
```

Or export it directly:

```
export GEMINI_API_KEY=your-key-here
```

## Usage

```
cleanmap input.png
# writes input.cleaned.png
```

Custom output path:

```
cleanmap input.png -o cleaned.png
```

Custom prompt:

```
cleanmap input.png -p "Remove all people. Keep the storefront."
```

## How it works

```
CLI → load image → Gemini 2.5 Flash Image (image + prompt) → save result
```
