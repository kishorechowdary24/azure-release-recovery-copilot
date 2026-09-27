import os

from dotenv import load_dotenv
from groq import Groq

load_dotenv()


def create_investigation_advice(
    service: str,
    error: str,
    recent_change: str,
    memories: list[str],
) -> str:
    if memories:
        memory_text = "\n".join(f"- {memory}" for memory in memories)
    else:
        memory_text = "No relevant past incident memories were found."

    client = Groq(api_key=os.environ["GROQ_API_KEY"])

    response = client.chat.completions.create(
        model="openai/gpt-oss-120b",
        reasoning_effort="low",
        max_completion_tokens=800,
        messages=[
            {
                "role": "system",
                "content": (
                    "You are a cautious deployment incident assistant. "
                    "A similar past incident is evidence, not proof of the "
                    "current cause. Do not say credentials are expired unless "
                    "the current incident confirms that. Do not invent product "
                    "details or assume a deployment platform unless the user "
                    "or a memory identifies it. Suggest safe checks for an "
                    "engineer to review; do not perform actions. Keep the "
                    "complete answer under 120 words and finish every section. "
                    "Use exactly these sections: Likely explanation (1-2 "
                    "sentences); Next checks (at most 3 bullets); How memory "
                    "helped (one sentence); Confidence (Low, Medium, or High "
                    "with a short reason, never a percentage). Use Medium "
                    "confidence when the current cause is not confirmed."
                ),
            },
            {
                "role": "user",
                "content": (
                    f"Service: {service or 'Not provided'}\n"
                    f"Deployment error: {error}\n"
                    f"Recent change: {recent_change or 'Not provided'}\n\n"
                    f"Recalled Hindsight memories:\n{memory_text}"
                ),
            },
        ],
    )

    return response.choices[0].message.content or "The model returned no advice."