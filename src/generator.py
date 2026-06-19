import os
from dotenv import load_dotenv
from google import genai

load_dotenv()

client = genai.Client(
    api_key=os.getenv("GEMINI_API_KEY")
)


def generate_response(
    user_query,
    persona,
    retrieved_chunks
):

    context = "\n\n".join(
        [chunk["content"] for chunk in retrieved_chunks]
    )

    if persona == "Technical Expert":

        persona_prompt = """
You are a Senior Systems Engineer.

Provide:
- Technical explanation
- Root cause analysis
- Detailed troubleshooting steps

Use ONLY the provided context.
"""

    elif persona == "Frustrated User":

        persona_prompt = """
You are an empathetic support specialist.

Provide:
- Empathy
- Simple language
- Clear action steps

Use ONLY the provided context.
"""

    else:

        persona_prompt = """
You are a Client Success Manager.

Provide:
- Concise response
- Business impact
- Resolution guidance

Use ONLY the provided context.
"""

    final_prompt = f"""
{persona_prompt}

Context:
{context}

User Question:
{user_query}
"""

    try:

        response = client.models.generate_content(
            model="gemini-2.5-flash",
            contents=final_prompt
        )

        return response.text

    except Exception as e:

        return (
            "The AI service is temporarily unavailable. "
            f"Error: {str(e)}"
        )


if __name__ == "__main__":

    sample_context = [
        {
            "content": """
Password Reset Guide

1. Go to Login Page.
2. Click Forgot Password.
3. Enter registered email.
4. Check inbox for reset link.
5. Create a new password.
"""
        }
    ]

    answer = generate_response(
        "How do I reset my password?",
        "Frustrated User",
        sample_context
    )

    print(answer)