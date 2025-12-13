print(">>> USING UPDATED LLM_UTILS FILE <<<")

from openai import OpenAI
from my_secrets import OPENAI_API_KEY


# Create a single OpenAI client we can reuse
client = OpenAI(api_key=OPENAI_API_KEY)


def summarize_text(text: str) -> str:
    """Summarize a piece of text in 2–4 sentences."""
    if not text.strip():
        return "Please enter some text to summarize in 2–4 sentences."

    prompt = f"Summarize this text in 2–4 sentences:\n\n{text}"

    response = client.responses.create(
        model="gpt-4o-mini",
        input=prompt,
        max_output_tokens=300,
    )
    return response.output_text


TUTOR_SYSTEM_PROMPT = (
    "You are a friendly programming tutor for first-year university students.\n\n"
    "You mainly help with:\n"
    "- Basic Python concepts (variables, loops, functions, errors).\n"
    "- Simple SQL and SQLite queries.\n"
    "- Understanding this project: a Streamlit app with login, SQLite and an AI summarizer/chatbot.\n\n"
    "When you answer:\n"
    "- Use clear, simple language.\n"
    "- Keep answers short (3–8 sentences).\n"
    "- If the user pastes code, briefly explain what it does and mention any obvious mistakes."
)


def chat_with_tutor(user_message: str, chat_history: list) -> str:
    """Simple multi-turn chatbot.

    chat_history is a list of dicts like:
    [{"role": "user"|"assistant", "content": "..."}]
    """
    if not user_message.strip():
        return "Please type a question so I can help you 🙂"

    # Turn the structured history into plain text that we send to the model
    history_lines = []
    for msg in chat_history:
        role = "User" if msg["role"] == "user" else "Tutor"
        history_lines.append(f"{role}: {msg['content']}")
    history_text = "\n".join(history_lines)

    full_prompt = (
        f"{TUTOR_SYSTEM_PROMPT}\n\n"
        f"Conversation so far:\n{history_text}\n\n"
        f"User: {user_message}\n"
        f"Tutor:"
    )

    response = client.responses.create(
        model="gpt-4o-mini",
        input=full_prompt,
        max_output_tokens=400,
    )
    return response.output_text
