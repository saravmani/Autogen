import openai
import pprint
from autogen import ConversableAgent
from transformers import pipeline

import os
from dotenv import load_dotenv

load_dotenv("config.env")  # Load environment variables from .env file

# OPENAI_API_KEY = os.getenv('OPENAI_API_KEY')  # Get the API key from the environment variable
LLM_STUDIO_BASEURL = os.getenv('LLM_STUDIO_BASEURL')  

# Open api 
# llm_config_openApi = {
#     "model": "gpt-3.5-turbo", 
#     "api_key": OPENAI_API_KEY,
#     "cache": None
#     }

# Local llm from LLM studio in my machine
llm_config_llmStudio = {
    "model":"hermes-3-llama-3.1-8b", #"llama-3.2-1b-instruct", # 
    "api_key": "lm-studio",
    "base_url":LLM_STUDIO_BASEURL,
    "cache": None    
    }




kingsMan = ConversableAgent(
    name="KingsMan",
    llm_config=llm_config_llmStudio,
    system_message="Your role is collect Name and Location information from the person who is chatting with you. And summarize in JSON Format {'name': '', 'location': ''}. ",
    human_input_mode="NEVER",
    is_termination_msg=lambda msg: "I gotta go" in msg["content"],
     max_consecutive_auto_reply=1
)

human_agent = ConversableAgent(
    name="human_agent",
    llm_config=False,
    code_execution_config=False,
    human_input_mode="ALWAYS",
)


chat_result = kingsMan.initiate_chat(
    recipient = human_agent, 
    message="what is your name", 
     summary_method="reflection_with_llm",
     summary_args={
        "summary_prompt" : "Return the customer information  (name and location)"
                             "into a JSON object only: use this JSON SCHEMA"
                             "{'name': '', 'location': ''}",
     }

)
pprint.pprint(chat_result.summary)
 