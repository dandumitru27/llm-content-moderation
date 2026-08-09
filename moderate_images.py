import base64
import json

from openai import OpenAI

from credentials import configure_api_keys

configure_api_keys()
client = OpenAI()

valid_image_path = "test_data/images/valid/mester_1_small.png"
sexual_image_path = "test_data/images/sexual/angelina_jolie_sexy.jpg"

with open(sexual_image_path, "rb") as f:
    image_base64 = base64.b64encode(f.read()).decode("utf-8")

response = client.moderations.create(
    model="omni-moderation-latest",
    input=[
        {
            "type": "image_url",
            "image_url": {"url": f"data:image/png;base64,{image_base64}"},
        }
    ],
)

result = response.results[0]
moderation_summary = {
    "flagged": result.flagged,
    "scores": {
        "hate": round(result.category_scores.hate, 2),
        "sexual": round(result.category_scores.sexual, 2),
        "violence": round(result.category_scores.violence, 2),
    },
}
print(
    json.dumps(
        moderation_summary,
        indent=2,
    )
)
