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
WELCOME_MESSAGE = (
    "Roaming Plan Assistant\n"
    "I'm here to help you find the best roaming plan for your upcoming trip.\n"
    "To get started, just let me know where you're traveling and for how long is your trip?"
)
REDIRECT_URL = "https://example.com/roaming-specialist"
LLM_MODEL_DEFAULT = "gpt-3.5-turbo"
RELEVANT_THRESHOLD_DEFAULT = 0.25
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
class BaseLLMIntentClassifier(BaseHandler):
    """
    A reusable base class for LLM-based binary or scored intent classification.

    Subclasses should supply:
    - a system prompt (instructions + examples)
    - an optional score threshold (default 0.5)
    """

    def __init__(self, llm=None, llm_model='', instructions=None, threshold=None, logging_level=None):
        load_dotenv()
        self.llm_model = llm_model or LLM_MODEL_DEFAULT
        self.llm = llm or ChatOpenAI(model=self.llm_model, temperature=0)
        self.instructions = instructions
        self.threshold: float = threshold or RELEVANT_THRESHOLD_DEFAULT
        self.logging_level = logging_level or LOGGING_LEVEL_DEFAULT

    def classify(self, user_input: str) -> dict:
        """
        Runs LLM classification on the given input.
        Returns:
            dict: {
                "score": float,
                "reason": str,
                "redirect": bool
            }
        """
        response = self.llm.invoke([
            SystemMessage(content=self.instructions),
            HumanMessage(content=user_input.strip())
        ])
        text = response.content.strip()
        lines = text.splitlines()

        reason = next((l for l in lines if l and not l.lower().startswith("score:")), "[no reasoning]")
        score_line = next((l for l in lines if l.lower().startswith("score:")), "Score: 0.0")

        try:
            score = float(score_line.split(":")[1].strip())
        except Exception:
            score = 0.0

        return {
            "reason": reason,
            "score": score,
            "redirect": score >= self.threshold
        }


class RoamingIntentClassifier(BaseLLMIntentClassifier):
    """
    A specialized intent classifier that detects roaming/mobile travel-related requests.
    """

    def __init__(self, llm=None, llm_model='', threshold=None, logging_level=None):
        super().__init__(
            llm_model=llm_model,
            llm=llm,
            instructions=AGENT_INSTRUCTIONS,
            threshold=threshold,
            logging_level=logging_level
        )


class DialogueManager(BaseHandler):
    """
    Self-contained conversation manager for CLI interaction.
    Handles classification, clarification, and optional redirect.
    """

    def __init__(self, welcome_message='', redirect_url=None, 
                 intent_classifier_llm_model='', intent_classifier_threshold='', logging_level=None):
        self.welcome_message = welcome_message or WELCOME_MESSAGE
        self.redirect_url = redirect_url or REDIRECT_URL
        self.logging_level = logging_level or LOGGING_LEVEL_DEFAULT
        self.intent_classifier_llm_model = intent_classifier_llm_model or LLM_MODEL_DEFAULT
        self.intent_classifier_threshold = intent_classifier_threshold or RELEVANT_THRESHOLD_DEFAULT
        self.classifier = RoamingIntentClassifier(
            llm_model=self.intent_classifier_llm_model, 
            logging_level=self.logging_level,
            threshold=self.intent_classifier_threshold
            )

    def step(self, user_input: str) -> dict:
        """
        Classify a single input. Returns response message and optional redirect.
        """
        result = self.classifier.classify(user_input)

        if self.logging_level == 0:
            print(f"Reason: {result['reason']}")
            print(f"Score: {result['score']}")

        if result["redirect"]:
            return {
                "message": "Great, let me forward you on to my associate!",
                "redirect": self.redirect_url
            }
        else:
            return {
                "message": "I'm here to help with roaming plans. Could you clarify your request?"
            }

    def run(self):
        """
        Launch the full CLI interaction loop.
        """
        print(self.welcome_message)

        while True:
            user_input = input("👤 You: ").strip()
            if user_input.lower() in {"exit", "quit"}:
                print("👋 Goodbye!")
                break

            response = self.step(user_input)
            print(f"Agent: {response['message']}")

            if "redirect" in response:
                print(response["redirect"])
                break


class RoamingPlanAgent(BaseHandler):
    def __init__(self):
        pass
