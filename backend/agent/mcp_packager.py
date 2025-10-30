
def package_mcp_context(question: str, retrieved_docs: list) -> str:
    system_instructions = (
        "You are a math tutor. Produce a step-by-step solution simplified for a high-school student. "
        "Cite sources. If content is not confirmed, return 'INSUFFICIENT_EXTERNAL_EVIDENCE'."
    )

    context_chunks = []
    for doc in retrieved_docs:
        chunk = f"Source: {doc['source']}\nContent: {doc['text']}\n"
        context_chunks.append(chunk)

    context = "\n---\n".join(context_chunks)

    prompt = f"""
System Instructions:
{system_instructions}

User Question:
{question}

Retrieved Context:
{context}
"""

    return prompt.strip()
