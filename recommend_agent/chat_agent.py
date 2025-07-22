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
    "Examples:\n"
    "User: I'm going to Japan, do you have data plans?\n"
    "Assistant: yes\n"
    "User: I want to know about your roaming services.\n"
    "Assistant: yes\n"
    "User: How much is it to call from Thailand?\n"
    "Assistant: yes\n"
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
