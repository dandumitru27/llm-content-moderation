import json
import os

from dotenv import load_dotenv
from langchain.agents import create_agent

from models import GEMINI_3_5_FLASH

accepted_languages = ["romanian", "hungarian", "english"]


def initialize_agent(model=GEMINI_3_5_FLASH, dbutils=None):
    if dbutils is not None:
        os.environ["OPENAI_API_KEY"] = dbutils.secrets.get(
            scope="MainSecretScope", key="OPENAI_API_KEY"
        )
        os.environ["GOOGLE_API_KEY"] = dbutils.secrets.get(
            scope="MainSecretScope", key="GOOGLE_API_KEY"
        )
        print("Using Databricks secrets")
    else:
        load_dotenv()

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
