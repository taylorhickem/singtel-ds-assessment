#!/usr/bin/env python3
"""Roaming Plan Recommendation Agent using LangChain
"""
# dependencies --------------------------------------------------------------------
from dotenv import load_dotenv
from base import BaseHandler
from langchain_openai import ChatOpenAI
from langchain.schema import SystemMessage, HumanMessage


# constants --------------------------------------------------------------------
WELCOME_LINE = (
    "Roaming Plan Assistant\n"
    "I'm here to help you find the best roaming plan for your upcoming trip.\n"
    "To get started, just let me know where you're traveling and for how long is your trip?"
)
REDIRECT_URL = "https://example.com/roaming-specialist"
LLM_MODEL = "gpt-3.5-turbo"
AGENT_INSTRUCTIONS = (
    "You're an assistant that classifies user intent. "
    "If the user is asking about mobile roaming, international travel SIMs, "
    "or data/call/SMS plans for a trip abroad, respond with 'yes'. "
    "Otherwise, respond with 'no'.\n\n"
    "Interpret generously. Include travel-related terms, misspellings, poor grammar, "
    "or references to specific places (cities, states, landmarks, etc).\n\n"
    "Here are some examples:\n"
    "\nUser: I'm going to Japan, do you have data plans?\nAssistant: yes"
    "\nUser: I want to know about your roaming services.\nAssistant: yes"
    "\nUser: How much is it to call from Thailand?\nAssistant: yes"
    "\nUser: 我去马来西亚旅行三天。\nAssistant: no"
    "\nUser: about 100GB \nAssistant: yes"
    "\nUser: I'm bringing my laptop \nAssistant: yes"
    "\nUser: I'm going to need a lot of data \nAssistant: yes"
    "\nUser: the vatican \nAssistant: yes"
    "\nUser: eight months \nAssistant: yes"
    "\nUser: I'm bringing my laptop and expect to work remote \nAssistant: yes"
    "\nUser: snorkeling in crystal clear waters\nAssistant: yes"
    "\nUser: visiting museums about Medieval European history\nAssistant: yes"
    "\nUser: attending a wedding in Bali\nAssistant: yes"
    "\nUser: backpacking through Europe\nAssistant: yes"
    "\nUser: vacationing with my family\nAssistant: yes"
    "\nUser: sightseeing for a few weeks\nAssistant: yes"
    "\nUser: remote work trip\nAssistant: yes"
    "\nUser: I'm planning a retreat\nAssistant: yes"
    "\nUser: I want a pony.\nAssistant: no"
    "\nUser: Stonehenge\nAssistant: yes"
    "\nUser: Paris\nAssistant: yes"
    "\nUser: Langkawi\nAssistant: yes"
    "\nUser: I need a lot of data\nAssistant: yes"
    "\nUser: What's the weather like in KL?\nAssistant: no"
)


AGENT_INSTRUCTIONS = (
    "You're an assistant that classifies user intent. "
    "If the user is asking about mobile roaming, international travel SIMs, "
    "or data/call/SMS plans for a trip abroad, respond with 'yes'. "
    "Otherwise, respond with 'no'.\n\n"
    "Consider a generous interpretation of something in the general vicinity of the topic and intention.\n"
    "Allow for cases of misspellings or incorrect grammar\n"
    "Consider any kind of geographic area or clue of a specific travel destination. A city, a landmark, a state, etc..\n"
    "Examples:\n"
    "User: I'm going to Japan, do you have data plans?\n"
    "Assistant: yes\n"
    "User: I want to know about your roaming services.\n"
    "Assistant: yes\n"
    "User: How much is it to call from Thailand?\n"
    "Assistant: yes\n"
    "User: I want a pony.\n"
    "Assistant: no\n"
    "我去马来西亚旅行三天。\n"
    "Assistant: no\n"
    "User: I'm bringing my laptop and expect to work remote\n"
    "Assistant: yes"
    "User: Maybe 100GB\n"
    "Assistant: yes"
    "User: I need a lot of data\n"
    "Assistant: yes"
    "User: eight months\n"
    "Assistant: yes"
    "User: Stonehenge\n"
    "Assistant: yes"
    "User: Paris\n"
    "Assistant: yes"
    "User: The vatican\n"
    "Assistant: yes"
    "User: Langkawi\n"
    "Assistant: yes"
    "User: Kosovo for a week.\n"
    "Assistant: yes"
    "User: I want a pony.\n"
    "Assistant: no\n"
    "User: What's the weather like in KL?\n"
    "Assistant: no\n"
)

# classes ----------------------------------------------------------------------------
class RoamingPlanAgent:

    def __init__(self, llm=None):
        load_dotenv()
        self.llm = llm or ChatOpenAI(model=LLM_MODEL, temperature=0)

    def step(self, user_msg: str) -> dict:
        system = AGENT_INSTRUCTIONS
        prompt = f"User: {user_msg.strip()}"

        response = self.llm.invoke([
            SystemMessage(content=system),
            HumanMessage(content=prompt)
        ])

        print(f'INFO. RAW LLM RESPONSE: \n {response.content}')

        answer = response.content.strip().lower()
        if "yes" in answer:
            return {
                "redirect": REDIRECT_URL,
                "message": "Great, let me forward you on to my associate!"
            }
        else:
            return {
                "message": "I'm here to help with roaming plans. Could you clarify your request?"
            }


class DialogueManager(BaseHandler):
    """Handles full CLI interaction with the RoamingPlanAgent."""

    def __init__(self, agent=None):
        self.agent = agent or RoamingPlanAgent()
        self.state = {}

    def step(self, msg: str) -> dict:
        result = self.agent.step(msg)
        self.state.update(result)
        return result

    def run_cli(self):
        print(WELCOME_LINE)
        print("Type 'exit' to quit.\n")

        while True:
            user_input = input("👤 You: ").strip()
            if user_input.lower() in ("exit", "quit"):
                print("👋 Goodbye!")
                break

            result = self.step(user_input)

            if "redirect" in result:
                print(result["message"])
                print(result["redirect"])
                break
            else:
                print(result["message"])
