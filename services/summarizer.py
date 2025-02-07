




import anthropic
import os
from transformers import pipeline  # Using Hugging Face's LLaMA model

# Load API key
anthropic_api_key = os.getenv("ANTHROPIC_API_KEY")
client = anthropic.Anthropic(api_key=anthropic_api_key)

# Load LLaMA Model for Free Summarization
llama_summarizer = pipeline("summarization", model="facebook/bart-large-cnn")  # Replace with actual LLaMA model if available

def should_summarize(text: str, threshold: int = 50) -> bool:
    """Check if the text length exceeds the threshold to decide whether summarization is needed."""
    return len(text.split()) > threshold


def summarize_text(text: str, model_type: str = "claude"):
    """
    Summarizes the given Turkish text using either Claude (high quality) or LLaMA (cost-effective).
    - `model_type='claude'`: Uses Claude Sonnet for high-quality summarization.
    - `model_type='llama'`: Uses LLaMA model for cost-saving summarization.
    """

    if model_type == "claude":
        system_instructions = """
        You are a Turkish language expert. Summarize the given Turkish text while keeping its core meaning intact.
        """

        user_message_text = f"Lütfen bu Türkçe metni özetle:\n<turkish_text>\n{text}\n</turkish_text>"

        response = client.messages.create(
            model="claude-3-5-sonnet-20241022",
            max_tokens=512,
            temperature=0.5,
            system=system_instructions,
            messages=[{"role": "user", "content": user_message_text}]
        )

        return response.content[0].text.strip() if response.content else ""

    elif model_type == "llama":
        return llama_summarizer(text, max_length=100, min_length=50, do_sample=False)[0]['summary_text']

    else:
        return "Invalid summarization model specified."

