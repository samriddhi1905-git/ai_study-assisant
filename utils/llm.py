from langchain_ollama import ChatOllama


def generate_answer(query, results):

    context = "\n\n".join(
        [doc.page_content for doc in results]
    )

    prompt = f"""
    Answer the question using ONLY the context below.

    Context:
    {context}

    Question:
    {query}
    """

    llm = ChatOllama(
        model="phi3",
        num_gpu=0
    )

    response = llm.invoke(prompt)

    return response.content