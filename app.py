import streamlit as st

from src.classifier import classify_persona
from src.generator import generate_response
from src.escalator import (
    should_escalate,
    generate_handoff_summary
)
from src.rag_pipeline import (
    LocalRAGPipeline,
    load_documents,
    chunk_documents
)

st.set_page_config(
    page_title="Persona Support Agent",
    page_icon="🤖"
)

st.title("🤖 Persona-Adaptive Customer Support Agent")

rag = LocalRAGPipeline()

# Build knowledge base automatically if empty
if rag.collection.count() == 0:
    docs = load_documents()
    chunks = chunk_documents(docs)
    rag.ingest_chunks(chunks)

st.write(f"Knowledge Base Documents: {rag.collection.count()}")

query = st.text_area(
    "Enter Customer Query"
)

if st.button("Submit"):

    if query.strip():

        with st.spinner("Analyzing customer query..."):

            persona_result = classify_persona(query)

            persona = persona_result["persona"]
            confidence = persona_result["confidence"]
            reasoning = persona_result["reasoning"]

            retrieved = rag.retrieve_context(query)

            escalated = should_escalate(
                query,
                retrieved
            )

        st.subheader("Detected Persona")
        st.success(persona)

        st.subheader("Confidence Score")
        st.info(f"{confidence:.2f}")

        st.subheader("Reasoning")
        st.write(reasoning)

        st.subheader("Retrieved Sources")

        if retrieved:

            for item in retrieved:
                st.write(f"📄 Source: {item['source']}")

                if "content" in item:
                    st.caption(item["content"][:200] + "...")

        else:
            st.warning("No documents retrieved.")

        if escalated:

            st.error("⚠️ ESCALATION REQUIRED")

            st.subheader("Human Handoff Summary")

            st.json(
                generate_handoff_summary(
                    persona,
                    query,
                    retrieved
                )
            )

        else:

            try:

                response = generate_response(
                    query,
                    persona,
                    retrieved
                )

                st.subheader("Generated Response")
                st.write(response)

            except Exception as e:

                st.error(
                    f"Response generation failed: {str(e)}"
                )

    else:

        st.warning("Please enter a customer query.")
