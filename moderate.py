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
    # "gpt-5-mini" / "gpt-5-nano"
    model = "gpt-5-mini"

    print(f"Using model: {model}")

    return create_agent(model)


def moderate_profile_description(ad_text, agent):

    prompt = f"""
        Esti un moderator de continut profesionist.

        Analizeaza urmatorul text al unui anunt adaugat de un mester pe o platforma de servicii 
        de mesteri (reparatii, renovari, constructii) si determina daca este:
        - Gibberish (text fara sens)
        - Spam (text care incearca sa promoveze ceva sau sa atraga atentia in mod nejustificat, 
        sau promoveaza servicii care nu sunt relevante pentru platforma de mesteri)
        - Inappropriate (text care contine limbaj ofensator, discriminare, sau alte elemente nepotrivite)
        - Language (limba in care este scris textul)

        "{ad_text}"

        Returneaza DOAR JSON valid in acest format:

        {{
        "is_gibberish": true/false,
        "is_spam": true/false,
        "is_inappropriate": true/false,
        "language": "detected language, in English, lowercase",
        "confidence": 0.0-1.0,
        "reason": "short explanation in maximum 10 words"
        }}
        """

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
