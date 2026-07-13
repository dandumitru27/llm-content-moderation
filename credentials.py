import os

from dotenv import load_dotenv


def configure_api_keys(dbutils=None):
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
