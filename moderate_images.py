import base64

from openai import OpenAI

from credentials import configure_api_keys

configure_api_keys()
client = OpenAI()

with open("test_data/images/valid/mester_1.png", "rb") as f:
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

print(response)
