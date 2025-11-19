from .db import db
from .config import config
import ollama

class Intelligence:
    def __init__(self):
        self.model = config.get("llm.query_model", "llama3.2:3b")

    def recall(self, query: str):
        # 1. Search database for relevant context
        results = db.search(query)
        context = "\n".join([f"[{r[1]}] {r[2]}: {r[3]}" for r in results])

        # 2. Ask LLM
        prompt = f"""
        Context from your history:
        {context}

        User Question: {query}

        Answer based on the context provided.
        """
        
        response = ollama.generate(model=self.model, prompt=prompt)
        return response['response']

intelligence = Intelligence()

