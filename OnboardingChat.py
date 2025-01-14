import openai
import pprint
from autogen import ConversableAgent
from autogen import initiate_chats

import os
from dotenv import load_dotenv

load_dotenv("config.env")  # Load environment variables from .env file
 
LLM_STUDIO_BASEURL = os.getenv('LLM_STUDIO_BASEURL')  
OPENAI_API_KEY = os.getenv('OPENAI_API_KEY')  # Get the API key from the environment variable
 

 
llm_config_openApi = {
    "model": "gpt-3.5-turbo", 
    "api_key": OPENAI_API_KEY,
    "cache": None
    }

# Local llm from LLM studio in my machine
llm_config_llmStudio = {
    "model": "hermes-3-llama-3.1-8b",#"hermes-3-llama-3.1-8b",#"llama-3.2-1b-instruct", # 
    "api_key": "lm-studio",
    "base_url":LLM_STUDIO_BASEURL,
    "cache": None  }


llm_config = llm_config_llmStudio


onboarding_personal_information_agent = ConversableAgent(
    name="Onboarding_Personal_Information_Agent",
    system_message='''You are a helpful customer onboarding agent,
    you work for a phone provider called ACME.
    Your job is to gather the customer's name and location.
    Do not ask for any other information, only ask about the customer's name and location.
    After the customer gives you their name and location, repeat them 
    and thank the user, and ask the user to answer with TERMINATE to move on to describing their issue.
    ''',
    llm_config=llm_config,
    human_input_mode="NEVER",
    is_termination_msg=lambda msg: "terminate" in msg.get("content").lower(),
    #  max_consecutive_auto_reply=2

)

onboarding_issue_agent = ConversableAgent(
    name="Onboarding_Issue_Agent",
    system_message='''You are a helpful customer onboarding agent,
    you work for a phone provider called ACME,
    you are here to help new customers get started with our product.
    Your job is to gather the product the customer use and the issue they currently 
    have with the product,
    Do not ask for other information.
    After the customer describes their issue, repeat it and add
    "Please answer with 'TERMINATE' if I have correctly understood your issue." ''',
    llm_config=llm_config,
    human_input_mode="NEVER",
    is_termination_msg=lambda msg: "terminate" in msg.get("content").lower()
)

customer_engagement_agent = ConversableAgent(
    name="Customer_Engagement_Agent",
    system_message='''You are a helpful customer service agent.
    Your job is to gather customer's preferences on news topics.
    You are here to provide fun and useful information to the customer based on the user's
    personal information and topic preferences.
    This could include fun facts, jokes, or interesting stories.
    Make sure to make it engaging and fun!
    Return 'TERMINATE' when you are done.''',
    llm_config=llm_config,
    human_input_mode="NEVER",
    is_termination_msg=lambda msg: "terminate" in msg.get("content").lower(),
    max_consecutive_auto_reply=2
)

# Human
human_agent = ConversableAgent(
    name="human_agent",
    llm_config=False,
    code_execution_config=False,
    human_input_mode="ALWAYS",
)

chats = [] # This is going to be our list of chats

chats.append(
    {
        "sender": onboarding_personal_information_agent,
        "recipient": human_agent,
        "message": 
            "Hello, I'm here to help you solve any issue you have with our products. "
            "Could you tell me your name?",
        "summary_method": "reflection_with_llm",
        "summary_args": {
         "summary_prompt" : "you are good in giving json resolts. now give me the user name and location in json format"
                             "{'name': '', 'location': ''}",
        },
        "clear_history" : True #the history will be transfered to the next chat
    }
)

chats.append(
    {
        "sender": onboarding_issue_agent,
        "recipient": human_agent,
        "message": 
                "Great! Could you tell me what issue you're "
                "currently having and with which product?",
        "summary_method": "reflection_with_llm",
        "clear_history" : False
    }
)

chats.append(
        {
        "sender": human_agent,
        "recipient": customer_engagement_agent,
        "message": "While we're waiting for a human agent to take over and help you solve "
        "your issue, can you tell me more about how you use our products or some "
        "topics interesting for you?",
        "max_turns": 2,
        "summary_method": "reflection_with_llm",
    }
)

chat_results = initiate_chats(chats)






for chat_result in chat_results:
    #pprint.pprint(chat_result.chat_history) # We could also get the whole chat history with this command
    pprint.pprint(chat_result.summary)