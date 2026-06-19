import os
import json
from dotenv import load_dotenv
from google import genai

load_dotenv()

client = genai.Client(
    api_key=os.getenv("GEMINI_API_KEY")
)


def classify_persona(user_message):

    prompt = f"""
Analyze the customer message.

Classify into EXACTLY one persona:

1. Technical Expert
2. Frustrated User
3. Business Executive

Return ONLY valid JSON in this format:

{{
    "persona": "...",
    "confidence": 0.0,
    "reasoning": "..."
}}

Customer Message:
{user_message}
"""

    try:

        response = client.models.generate_content(
            model="gemini-2.5-flash",
            contents=prompt
        )

        cleaned_text = (
            response.text
            .replace("```json", "")
            .replace("```", "")
            .strip()
        )

        return json.loads(cleaned_text)

    except Exception as e:

        return {
            "persona": "Frustrated User",
            "confidence": 0.0,
            "reasoning": f"Gemini API Error: {str(e)}"
        }


if __name__ == "__main__":

    msg = (
        "Our API returns a 401 Unauthorized error. "
        "Can you explain the authentication failure?"
    )

    result = classify_persona(msg)

    print(json.dumps(result, indent=2))