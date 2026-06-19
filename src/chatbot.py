from classifier import classify_persona
from generator import generate_response
from escalator import (
    should_escalate,
    generate_handoff_summary
)
from rag_pipeline import (
    LocalRAGPipeline,
    load_documents,
    chunk_documents
)


print("Customer Support Agent")
print("Type 'exit' to quit")

docs = load_documents()

chunks = chunk_documents(docs)

rag = LocalRAGPipeline()

while True:

    query = input("\nUser: ")

    if query.lower() == "exit":
        break

    persona_result = classify_persona(query)
    persona = persona_result["persona"]

    retrieved = rag.retrieve_context(query)

    escalated = should_escalate(
        query,
        retrieved
    )

    print("\nDetected Persona:")
    print(persona)

    print("\nRetrieved Sources:")
    for item in retrieved:
        print("-", item["source"])

    if escalated:

        print("\nESCALATION REQUIRED")

        print(
            generate_handoff_summary(
                persona,
                query,
                retrieved
            )
        )

        continue

    answer = generate_response(
        query,
        persona,
        retrieved
    )

    print("\nResponse:")
    print(answer)