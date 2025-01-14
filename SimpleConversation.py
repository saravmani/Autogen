import openai
import pprint
from autogen import ConversableAgent
from transformers import pipeline

import os
from dotenv import load_dotenv

load_dotenv("config.env")  # Load environment variables from .env file

OPENAI_API_KEY = os.getenv('OPENAI_API_KEY')  # Get the API key from the environment variable
LLM_STUDIO_BASEURL = os.getenv('LLM_STUDIO_BASEURL')  

# Open api 
# llm_config_openApi = {
#     "model": "gpt-3.5-turbo", 
#     "api_key": OPENAI_API_KEY,
#     "cache": None
#     }

# Local llm from LLM studio in my machine
llm_config_llmStudio = {
    "model": "llama-3.2-1b-instruct", # 
    "api_key": "lm-studio",
    "base_url":LLM_STUDIO_BASEURL,
    "cache": None    
    }




kingsMan = ConversableAgent(
    name="KingsMan",
    llm_config=llm_config_llmStudio,
    system_message="Your name is kingsMan and you are a stand-up comedian in a two-person comedy show. "
    "When you're ready to end the conversation, say 'I gotta go'.",
    human_input_mode="NEVER",
    is_termination_msg=lambda msg: "I gotta go" in msg["content"],
     max_consecutive_auto_reply=1
)
scorpionKing = ConversableAgent(
    name="ScorpionKing",
    llm_config=llm_config_llmStudio,
    system_message="Your name is ScorpionKing and you are very strict person and want to terminate the conversation as soon as possible. "
    "When you're ready to end the conversation, say 'I gotta go'.",
    human_input_mode="NEVER",
    is_termination_msg=lambda msg: "I gotta go" in msg["content"],
    max_consecutive_auto_reply=1
)

chat_result = kingsMan.initiate_chat(
    recipient = scorpionKing, 
    message="I'm kingsMan. ScorpionKing, let's keep the jokes rolling, let's start with jokes about therapists.", 
)
pprint.pprint(chat_result.summary)

# if needed we can start the conversation agian with below lines
# scorpionKing.send(message="What's the last joke we talked about?", recipient=kingsMan)