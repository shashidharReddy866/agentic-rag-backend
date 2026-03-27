from .gemini_llm import ask_gemini

def agent(query, retriever):

    # Agentic Multi-Query: Split compound questions into independent searches
    sub_queries = [q.strip() + "?" for q in query.split("?") if len(q.strip()) > 2]
    if not sub_queries:
        sub_queries = [query]
        
    all_docs = []
    for sub_q in sub_queries:
        all_docs.extend(retriever.invoke(sub_q))
        
    # Deduplicate chunks to keep context window efficient
    unique_chunks = list(set([doc.page_content for doc in all_docs]))
    context = "\n\n".join(unique_chunks)

    # Agentic behavior
    if "summary" in query.lower():
        prompt = f"Summarize the following:\n{context}"
    
    elif "extract" in query.lower():
        prompt = f"Extract key information from:\n{context}"
    
    else:
        prompt = f"""
        You are an intelligent document assistant.

        Context:
        {context}

        Question:
        {query}

        Extract the requested information accurately. 
        You MUST respond ONLY with a valid JSON object.
        Each requested piece of information should be its own key-value pair in the JSON.
        Do NOT wrap the JSON in markdown ticks (e.g. no ```json). Just output the raw JSON object.
        If a piece of information is not found, set its value to null.
        """

    return ask_gemini(prompt)
