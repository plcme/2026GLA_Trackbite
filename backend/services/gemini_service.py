import os
from google import genai
from google.genai import types

_client: genai.Client | None = None


def get_client() -> genai.Client:
    global _client
    if _client is None:
        project = os.environ.get("GOOGLE_CLOUD_PROJECT")
        location = os.environ.get("GOOGLE_CLOUD_LOCATION", "us-central1")
        credentials_path = os.environ.get("GOOGLE_APPLICATION_CREDENTIALS")

        if not project:
            raise ValueError("GOOGLE_CLOUD_PROJECT environment variable is not set")
        
        # Google SDK will automatically look for GOOGLE_APPLICATION_CREDENTIALS file
        _client = genai.Client(
            vertexai=True,
            project=project,
            location=location,
        )
    return _client


async def test_prompt(prompt: str) -> str:
    client = get_client()
    model = os.environ.get("GEMINI_MODEL", "gemini-3-flash-preview")

    response = client.models.generate_content(
        model=model,
        contents=prompt,
        config=types.GenerateContentConfig(
            temperature=0.7,
            max_output_tokens=256,
        ),
    )
    return response.text
