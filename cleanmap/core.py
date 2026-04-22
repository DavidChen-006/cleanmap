import mimetypes
import os
from pathlib import Path

from google import genai
from google.genai import types

MODEL = "gemini-2.5-flash-image"

DEFAULT_PROMPT = (
    "Extract the main building or primary subject. "
    "Remove clutter like cars, people, trees, signs, and power lines. "
    "Preserve lighting and perspective. Return a clean edited image."
)


def clean_image(input_path, output_path, prompt=DEFAULT_PROMPT):
    api_key = os.environ.get("GEMINI_API_KEY")
    if not api_key:
        raise RuntimeError("GEMINI_API_KEY not set.")

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
