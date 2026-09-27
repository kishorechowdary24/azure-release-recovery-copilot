import os

from dotenv import load_dotenv
from hindsight_client import Hindsight

load_dotenv()

incidents = [
    (
        "INC-002",
        "A deployment received a permission-denied error. "
        "The credential was valid, but the service connection lacked "
        "the required permission on the target resource group. "
        "An authorized owner granted the needed permission, and the "
        "deployment then succeeded.",
    ),
    (
        "INC-003",
        "A release could not find the target web app. The service "
        "connection was valid, but the pipeline selected the wrong "
        "Azure subscription. The team selected the subscription that "
        "contained the web app, and the deployment succeeded.",
    ),
    (
        "INC-004",
        "A release deployed an older build than expected because the "
        "pipeline used an artifact from a previous build. The team "
        "updated the release to use the artifact from the current build, "
        "and the expected version was deployed.",
    ),
    (
        "INC-005",
        "The web app deployment completed, but the app failed its health "
        "check because a required application setting was missing. "
        "The team added the setting and restarted the app; the health "
        "check then passed.",
    ),
]

client = Hindsight(
    base_url=os.environ["HINDSIGHT_BASE_URL"],
    api_key=os.environ["HINDSIGHT_API_KEY"],
)

try:
    bank_id = os.environ["HINDSIGHT_BANK_ID"]

    for incident_id, details in incidents:
        client.retain(
            bank_id=bank_id,
            content=f"Resolved incident {incident_id}: {details}",
            context=f"Azure release incident {incident_id}",
        )
        print(f"Saved {incident_id}")

    print("Finished adding the sample incidents.")
finally:
    client.close()