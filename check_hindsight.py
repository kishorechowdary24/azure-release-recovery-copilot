import os

from dotenv import load_dotenv
from hindsight_client import Hindsight

load_dotenv()

client = Hindsight(
    base_url=os.environ["HINDSIGHT_BASE_URL"],
    api_key=os.environ["HINDSIGHT_API_KEY"],
)

bank_id = os.environ["HINDSIGHT_BANK_ID"]

client.retain(
    bank_id=bank_id,
    content=(
        "Incident INC-001: An Azure deployment failed because the "
        "service connection credential had expired. The engineer renewed "
        "the credential and reran the deployment. The deployment succeeded."
    ),
)

result = client.recall(
    bank_id=bank_id,
    query="How was the deployment failure caused by expired credentials fixed?",
)

print("Hindsight connection worked.")
print("Memories found:")
for memory in result.results:
    print("-", memory.text)

client.close()