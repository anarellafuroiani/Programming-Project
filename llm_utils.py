print(">>> USING UPDATED LLM_UTILS FILE <<<")
from openai import OpenAI
from secrets import OPENAI_API_KEY

def summarize_text(text):
    if not text.strip():
        return "Please enter some text."

    client = OpenAI(api_key=OPENAI_API_KEY)

    response = client.responses.create(
        model="gpt-4o-mini",
        input=f"Summarize this text in 4–5 sentences:\n\n{text}"
    )

    return response.output_text
