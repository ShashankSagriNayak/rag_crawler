import os
import time
import google.generativeai as genai
from src.retriever import Retriever # Assuming this is your custom retriever class
from dotenv import load_dotenv
# Load environment variables from .env
load_dotenv()

# Configure the Gemini API key once when the application starts
genai.configure(api_key=os.getenv("GEMINI_API_KEY"))

class QAService:
    def __init__(self):
        """
        Initializes the retriever and the Gemini generative model.
        The model is created only once for efficiency.
        """
        self.retriever = Retriever()

        # EFFICIENT: Initialize the model once and reuse it.
        # Use a valid model name like 'gemini-1.5-pro-latest' or 'gemini-1.5-flash-latest'.
        self.model = genai.GenerativeModel('gemini-2.5-flash-lite')

        # Define generation configuration
        self.generation_config = genai.types.GenerationConfig(
            max_output_tokens=500,
            # You can add other parameters like temperature, top_p, etc. here
            # temperature=0.7
        )

    def build_prompt(self, question, retrieved):
        """Builds the prompt for the generative model."""
        context = "\n\n".join([r["snippet"] for r in retrieved])
        return f"""
You are a helpful assistant that must answer strictly from the provided context.
If the context does not contain enough information, say exactly:
"Not found in crawled content."

Context:
{context}

Question: {question}
Answer:
"""

    def ask(self, question, top_k=3):
        """Performs retrieval and generation to answer a question."""
        start = time.time()
        retrieved = self.retriever.retrieve(question, top_k)
        retrieval_ms = int((time.time() - start) * 1000)

        prompt = self.build_prompt(question, retrieved)
        gen_start = time.time()

        # --- CORRECTED GEMINI API CALL ---
        # 1. Call generate_content on the model instance created in __init__.
        # 2. Pass the generation_config for parameters like max_output_tokens.
        response = self.model.generate_content(
            prompt,
            generation_config=self.generation_config
        )

        # 3. Access the generated text using the .text attribute.
        answer = response.text.strip()
        generation_ms = int((time.time() - gen_start) * 1000)
        total_ms = int((time.time() - start) * 1000)

        return {
            "answer": answer,
            "sources": [{"url": r["url"], "snippet": r["snippet"][:200]} for r in retrieved],
            "timings": {"retrieval_ms": retrieval_ms, "generation_ms": generation_ms, "total_ms": total_ms},
        }