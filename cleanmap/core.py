import mimetypes
import os
from pathlib import Path

from google import genai
from google.genai import types

MODEL = "gemini-2.5-flash-image"

DEFAULT_PROMPT = (
    
    "Remove all obstructions blocking the view of the building: cars, people, "
    "trees, signs, utility poles, and power lines. Seamlessly fill the vacated "
    "areas by continuing the building's own patterns and the surrounding "
    "environment. Keep everything else in the image exactly the same — the "
    "building's position, size, framing, lighting, shadows, time of day, sky, "
    "and perspective must be identical to the original. Return a clean edited "
    "photo of the unobstructed building."
)


def clean_image(input_path, output_path, prompt=DEFAULT_PROMPT):
    api_key = os.environ.get("GEMINI_API_KEY")
    if not api_key:
        raise RuntimeError(
            "GEMINI_API_KEY not set.\n"
            "  - Easiest: pass it on the command line: cleanmap <image> --api-key YOUR_KEY\n"
            "  - Or create a .env file in your current directory with: GEMINI_API_KEY=your-key\n"
            "  - Or set it for the session:\n"
            "      PowerShell: $env:GEMINI_API_KEY = \"your-key\"\n"
            "      macOS/Linux: export GEMINI_API_KEY=your-key\n"
            "  - If you used `setx GEMINI_API_KEY ...`, close and reopen PowerShell, then retry.\n"
            "  - Get a free key: https://aistudio.google.com/apikey"
        )

    image_bytes = Path(input_path).read_bytes()
    mime_type = mimetypes.guess_type(input_path)[0] or "image/png"

    client = genai.Client(api_key=api_key)
    response = client.models.generate_content(
        model=MODEL,
        contents=[
            types.Part.from_bytes(data=image_bytes, mime_type=mime_type),
            prompt,
        ],
    )

    for candidate in response.candidates or []:
        for part in candidate.content.parts or []:
            if getattr(part, "inline_data", None) and part.inline_data.data:
                Path(output_path).write_bytes(part.inline_data.data)
                return

    raise RuntimeError("Model returned no image.")
