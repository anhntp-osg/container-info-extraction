import json
import os

from google import genai
from google.genai import types

from .classifier import classify_container_type
from .models import ContainerInfo

GEMINI_MODEL = "gemini-2.5-flash"

_ANALYZE_PROMPT = """Analyze this image and respond ONLY with a JSON object (no markdown, no explanation).

If this is NOT a container image, respond with:
{"is_container": false}

If this IS a container image, respond with:
{
  "is_container": true,
  "container_id": "<the container code/ID visible on the container, or null if not visible>",
  "container_type_description": "<describe the container type, e.g. 20ft, 40ft, high cube, reefer, gp, dry van, etc., or null if unknown>"
}"""


def _get_client() -> genai.Client:
    api_key = os.environ.get("GOOGLE_API_KEY")
    if not api_key:
        raise EnvironmentError("GOOGLE_API_KEY is not set. Check your .env file.")
    return genai.Client(api_key=api_key)


def _parse_gemini_response(raw: str) -> dict:
    """Strip optional markdown fences and parse JSON from Gemini response."""
    raw = raw.strip()
    if raw.startswith("```"):
        parts = raw.split("```")
        raw = parts[1].lstrip("json").strip()
    return json.loads(raw)


def _normalize_null(value: str | None) -> str | None:
    """Convert Gemini's string 'null'/'Null' to Python None."""
    if value and value.lower() == "null":
        return None
    return value


def analyze_container_image(image_path: str, mime_type: str = "image/jpeg") -> ContainerInfo:
    """Send an image to Gemini and return structured ContainerInfo."""
    client = _get_client()

    with open(image_path, "rb") as f:
        image_bytes = f.read()

    response = client.models.generate_content(
        model=GEMINI_MODEL,
        contents=[
            _ANALYZE_PROMPT,
            types.Part.from_bytes(data=image_bytes, mime_type=mime_type),
        ],
    )

    data = _parse_gemini_response(response.text)

    if not data.get("is_container"):
        return ContainerInfo(is_container=False)

    container_id = _normalize_null(data.get("container_id"))
    type_desc = _normalize_null(data.get("container_type_description"))

    info = ContainerInfo(
        is_container=True,
        container_id=container_id,
        container_type_description=type_desc,
    )

    # if container_id is not None and not info.is_osg:
    if not info.is_osg:
        info.container_type = classify_container_type(type_desc)

    return info
