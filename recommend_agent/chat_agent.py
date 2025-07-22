#!/usr/bin/env python3
"""Roaming Plan Recommendation Agent using LangChain
"""
# dependencies --------------------------------------------------------------------
from dotenv import load_dotenv
from base import BaseHandler
from langchain_openai import ChatOpenAI
from langchain.schema import SystemMessage, HumanMessage


# constants --------------------------------------------------------------------
LOGGING_LEVEL_DEFAULT = 1
WELCOME_LINE = (
    "Roaming Plan Assistant\n"
    "I'm here to help you find the best roaming plan for your upcoming trip.\n"
    "To get started, just let me know where you're traveling and for how long is your trip?"
)
REDIRECT_URL = "https://example.com/roaming-specialist"
LLM_MODEL = "gpt-3.5-turbo"
RELEVANT_THRESHOLD_DEFAULT = 0.33
AGENT_INSTRUCTIONS = (
    "You're an assistant that determines how likely it is that a user is asking about mobile roaming, "
    "international SIM cards, or travel-related data/call/SMS services.\n\n"
    "First, explain your reasoning in 1 sentence.\n"
    "Then output a relevance score between 0.0 and 1.0 on a new line, labeled as 'Score:'.\n"
    "Interpret generously. Include travel-related terms, misspellings, poor grammar, "
    "or references to specific places (cities, states, landmarks, etc).\n\n"
    "Examples:\n"
    "User: I'm going to Japan, do you have data plans?\n"
    "Reasoning: This user is clearly asking about international mobile service.\n"
    "Score: 1.0\n\n"
    "User: Vallhalla for a month\n"
    "Reasoning: Vallhalla is not a real travel destination for mobile networks.\n"
    "Score: 0.0\n\n"
    "User: snorkeling in crystal clear waters\n"
    "Reasoning: This suggests a travel scenario but needs further clarification to determine mobile needs.\n"
    "Score: 0.6\n\n"
    "User: Paris\n"
    "Reasoning: Paris is a valid travel destination, implying potential roaming needs.\n"
    "Score: 0.85\n\n"
    "User: #我去马来西亚旅行三天。\n"
    "Reasoning: Although it's a valid prompt when translated to English, we are limiting only to English.\n"
    "Score: 0.0\n\n"
    "User: Paris\n"
    "Reasoning: Paris is a valid travel destination, implying potential roaming needs.\n"
    "Score: 0.85\n\n"
    "User: What's the weather like in KL?\n"
    "Reasoning: KL is shorthand for Kuala Lumpur, Malaysia and is a valid travel destination, implying potential roaming needs.\n"
    "Score: 0.85\n\n"
    "User: Paris\n"
    "Reasoning: Paris is a valid travel destination, implying potential roaming needs.\n"
    "Score: 0.85\n\n"
    "User: I'm hungry\n"
    "Reasoning: This is clearly off topic.\n"
    "Score: 0.0\n\n"
    "User: I want a pony\n"
    "Reasoning: This is clearly off topic\n"
    "Score: 0.0\n\n"
    "User: I need a lot of data\n"
    "Reasoning: Mentions data so potentially relevant for a data plan.\n"
    "Score: 0.7\n\n"
    "User: remote work for 6 months\n"
    "Reasoning: Remote working would have data plan needs so this is relevant.\n"
    "Score: 0.8\n\n"
    "User: visiting family\n"
    "Reasoning: Visiting family is a type of travel and thus relevant.\n"
    "Score: 0.85\n\n"
    "User: I'm bringing my laptop\n"
    "Reasoning: Suggestive of travel need more details to confirm.\n"
    "Score: 0.6\n\n"
    "User: I need a lot of data\n"
    "Reasoning: They need data so thats relevant will need to prompt them further to get to specifics.\n"
    "Score: 0.7\n\n"
    "User: Unknown Soldier\n"
    "Reasoning: Too vauge that could mean anything.\n"
    "Score: 0.0\n\n"
    "User: Tomb of the Unknown Soldier\n"
    "Reasoning: Those are specific landmark destinations for travel, albeit there are more than one.\n"
    "Score: 0.7\n\n"
    "User: meditation in the Himalayas\n"
    "Reasoning: A valid travel destination and thus relevant.\n"
    "Score: 0.85\n\n"
)


# classes ----------------------------------------------------------------------------
class RoamingPlanAgent:

    def __init__(self, llm=None, logging_level=None, relevant_threshold=None):        
        load_dotenv()
        self.llm = llm or ChatOpenAI(model=LLM_MODEL, temperature=0)
        self.redirect_url = REDIRECT_URL
        self.relevant_threshold = relevant_threshold or RELEVANT_THRESHOLD_DEFAULT
        self.logging_level: int = logging_level or LOGGING_LEVEL_DEFAULT 

    def step(self, user_msg: str) -> dict:
        system = AGENT_INSTRUCTIONS
        prompt = f"User: {user_msg.strip()}"

        response = self.llm.invoke([
            SystemMessage(content=system),
            HumanMessage(content=prompt)
        ])

        lines = response.content.strip().splitlines()
        reason_line = next((line for line in lines if not line.lower().startswith("score:")), None)
        score_line = next((line for line in lines if line.lower().startswith("score:")), None)

        try:
            score = float(score_line.split(":")[1].strip()) if score_line else 0.0
        except Exception:
            score = 0.0

        if self.logging_level == 0:
            print(f'INFO. LLM reasoning: {reason_line}')
            print(f'INFO. LLM score: {score}')

        if score > self.relevant_threshold:
            return {
                "redirect": self.redirect_url,
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
