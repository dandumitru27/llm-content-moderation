import json
import os

from dotenv import load_dotenv
from langchain.agents import create_agent

accepted_languages = ["romanian", "hungarian", "english"]


def initialize_agent():
    use_databricks = False

    if use_databricks:
        os.environ["OPENAI_API_KEY"] = dbutils.secrets.get(
            scope="MainSecretScope", key="OPENAI_API_KEY"
        )
        os.environ["GOOGLE_API_KEY"] = dbutils.secrets.get(
            scope="MainSecretScope", key="GOOGLE_API_KEY"
        )
    else:
        load_dotenv()

    # "google_genai:gemini-3-flash-preview"
    # "gpt-5-mini" / "gpt-5-nano" / "gpt-5.4-nano"
    model = "google_genai:gemini-3-flash-preview"

    print(f"Using model: {model}")

    return create_agent(model)


PROMPT_DIR = os.path.join(os.path.dirname(__file__), "prompts")


def moderate_profile_description(ad_text, agent):

    with open(
        os.path.join(PROMPT_DIR, "moderate_profile_description.txt"), encoding="utf-8"
    ) as f:
        prompt = f.read().format(ad_text=ad_text)

    response = agent.invoke({"messages": [{"role": "user", "content": prompt}]})

    content = response["messages"][-1].content

    if isinstance(content, list):
        text = content[0]["text"]
    else:
        text = content

    evaluation = json.loads(text)

    is_valid = (
        not evaluation["is_gibberish"]
        and not evaluation["is_spam"]
        and not evaluation["is_inappropriate"]
        and evaluation["language"] in accepted_languages
    )

    evaluation = {
        "is_valid": is_valid,
        **evaluation,
    }

    return evaluation
