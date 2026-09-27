import os

from dotenv import load_dotenv
from hindsight_client import Hindsight

load_dotenv()


def find_similar_incidents(query: str) -> list[str]:
    client = Hindsight(
        base_url=os.environ["HINDSIGHT_BASE_URL"],
        api_key=os.environ["HINDSIGHT_API_KEY"],
    )

    try:
        result = client.recall(
            bank_id=os.environ["HINDSIGHT_BANK_ID"],
            query=query,
            budget="high",
            max_tokens=4096,
        )
        return [memory.text for memory in result.results[:2]]
    finally:
        client.close()


def retain_resolved_incident(
    service: str,
    error: str,
    recent_change: str,
    cause: str,
    fix: str,
    outcome: str,
) -> None:
    content = (
        f"Resolved deployment incident.\n"
        f"Service: {service or 'Not provided'}\n"
        f"Error: {error}\n"
        f"Recent change: {recent_change or 'Not provided'}\n"
        f"Actual cause: {cause}\n"
        f"Fix applied: {fix}\n"
        f"Outcome: {outcome}"
    )

    client = Hindsight(
        base_url=os.environ["HINDSIGHT_BASE_URL"],
        api_key=os.environ["HINDSIGHT_API_KEY"],
    )

    try:
        client.retain(
            bank_id=os.environ["HINDSIGHT_BANK_ID"],
            content=content,
            context="Resolved deployment incident",
        )
    finally:
        client.close()
