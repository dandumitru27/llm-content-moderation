# llm-content-moderation

LLM Content Moderation for user-generated content: profile descriptions, reviews, photos etc. Python, LangChain, optionally Databricks.

## Initial setup

~ new virtual environment  
py -3.10 -m venv .venv

~ activate env  
.venv\Scripts\activate.bat

~ install all dependencies  
poetry install

~ prepare .env file  
Make a copy of the provided `.env.template` file, rename it to `.env` and put there your secret keys, you can also use only one of GOOGLE_API_KEY and OPENAI_API_KEY.

## Helpful commands

~ add new package  
poetry add package-name
