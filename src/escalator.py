import json
from datetime import datetime

def should_escalate(query, retrieved_chunks):

    sensitive_keywords = [
        "billing",
        "refund",
        "legal",
        "lawsuit",
        "duplicate charge",
        "payment dispute",
        "account breach",
        "unauthorized transaction",
        "account hacked",
        "identity theft",
        "data breach",
        "security incident",
        "privacy violation",
        "regulatory compliance",
        "fraud"
    ]

    query_lower = query.lower()

    # Sensitive issues -> escalate
    for keyword in sensitive_keywords:
        if keyword in query_lower:
            return True

    # No relevant KB info found
    if len(retrieved_chunks) == 0:
        return True

    return False


def generate_handoff_summary(
    persona,
    query,
    retrieved_chunks
):

    summary = {
        "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        "persona": persona,
        "issue": query,
        "conversation_history": [query],
        "documents_used": [
            chunk["source"]
            for chunk in retrieved_chunks
        ],
        "attempted_steps": [
            "Persona detection completed",
            "Knowledge base retrieval completed",
            "Adaptive response generation attempted"
        ],
        "recommendation":
        "Escalate to human support for further investigation."
    }

    return json.dumps(summary, indent=2)
