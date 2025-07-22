#!/usr/bin/env python3
"""Roaming Plan Recommendation Agent using LangChain
"""

# dependencies -------------------------------------------------------------------
from typing import Optional
import re
import pandas as pd
from base import BaseHandler
from .recommend import RoamingPlanRecommender

# langchain imports
from langchain_openai import ChatOpenAI
from langchain.memory import ConversationBufferMemory
from langchain.prompts import ChatPromptTemplate, MessagesPlaceholder
from langchain.schema import SystemMessage
from langchain.agents import AgentExecutor, create_openai_functions_agent
from langchain.tools import StructuredTool
from pydantic import BaseModel, Field


# constants ---------------------------------------------------------------------------------------
VERBOSE = True
AGENT_SYSTEM_MESSAGE="""You are a helpful assistant that recommends roaming plans.
    Ask the user questions to gather the following fields: "
    destination, duration in days, service type (data/calls/sms), and data amount in GB if applicable.
    Use the `roaming_plan_recommend` tool only once all required fields are collected.
    If the user provides you with nonsense or irrelevant response, politely redirect them back on topic.
    If after 3x failed attempts to redirect them, proceed to exit and suggest they contact Singtel support for further assistance.
"""

# classes ---------------------------------------------------------------------------------------
class RecommendInput(BaseModel):
    destination: str = Field(..., description="Country where the user will travel")
    duration_days: int = Field(..., description="Trip duration in days")
    service_type: str = Field("data", description="Service type: data, calls or sms")
    data_needed_gb: Optional[float] = Field(None, description="Data needed in GB if service is data")


class RoamingPlanAgent(BaseHandler):
    """Conversational roaming plan assistant implemented with LangChain."""

    def __init__(self, recommender: RoamingPlanRecommender = None, llm: ChatOpenAI = None):
        self.recommender = recommender or RoamingPlanRecommender()
        # ensure database is available
        self.recommender.db_build()
        self._load_destinations()
        self.llm = llm or self._default_llm()
        self.memory = ConversationBufferMemory(memory_key="chat_history", return_messages=True)
        self.tool = StructuredTool.from_function(
            func=self._tool_recommend,
            name="roaming_plan_recommend",
            description="Recommend roaming plans for a travel query",
            args_schema=RecommendInput,
            return_direct=False,
        )

        self.agent_executor = self._init_agent() if self.llm else None
        self.reset()
        super().__init__()

    def _default_llm(self):
        try:
            return ChatOpenAI(model="gpt-3.5-turbo", temperature=0)
        except Exception:
            return None

    def _init_agent(self):
        prompt = ChatPromptTemplate.from_messages([
            SystemMessage(content=AGENT_SYSTEM_MESSAGE),
            MessagesPlaceholder(variable_name="chat_history"),
            MessagesPlaceholder(variable_name="agent_scratchpad"),
        ])
        agent = create_openai_functions_agent(self.llm, [self.tool], prompt)
        self.agent_executor = AgentExecutor(
            agent=agent,
            tools=[self.tool],
            memory=self.memory,
            verbose=VERBOSE 
        )
        return self.agent_executor

    def _tool_recommend(self, destination: str, duration_days: int, service_type: str = "data", data_needed_gb: Optional[float] = None):
        # update state from tool call
        self.state["destination"] = destination
        self.state["duration_days"] = duration_days
        self.state["service_type"] = service_type
        self.state["data_needed_gb"] = data_needed_gb
        plans = self.recommender.recommend(destination, duration_days, service_type, data_needed_gb)
        self.state["plans"] = plans
        return plans

    def _load_destinations(self):
        self._dest_lookup = self.recommender.get_destinations()

    def reset(self):
        """Clear conversation state."""
        self.state = {
            'destination': '',
            'duration_days': None,
            'service_type': 'data',
            'data_needed_gb': None,
            'plans': [],
            'selected_plan': None,
        }

    # parsing  ----------------------------------------------------------------
    def _parse_destination(self, text: str) -> str:
        match = re.search(r'(?:to|in|for) ([A-Za-z ]+?)(?:\b|,| for|$)', text)
        if match:
            dest = match.group(1).strip()
            return dest
        return ''

    def _canonical_destination(self, dest: str) -> str:
        dest_lc = dest.lower()
        if dest_lc in self._dest_lookup:
            return self._dest_lookup[dest_lc]
        if dest_lc == 'korea':
            return 'Korea, Republic of'
        return ''

    def _parse_duration(self, text: str) -> Optional[int]:
        m = re.search(r'(\d+)\s*(day|days|week|weeks|month|months)', text)
        if m:
            num = int(m.group(1))
            unit = m.group(2)
            if unit.startswith('week'):
                return num * 7
            if unit.startswith('month'):
                return num * 30
            return num
        return None

    def _parse_data_amount(self, text: str) -> Optional[float]:
        m = re.search(r'(\d+(?:\.\d+)?)\s*gb', text.lower())
        if m:
            return float(m.group(1))
        return None

    def _parse_service_type(self, text: str) -> str:
        txt = text.lower()
        if 'sms' in txt:
            return 'sms'
        if 'call' in txt:
            return 'calls'
        if 'data' in txt:
            return 'data'
        return ''

    # ---------------------------------------------------------------- interaction
    def step(self, user_message: str) -> dict:
        """Process one user message and return agent response state."""
        msg = user_message.strip()

        # check if user selected a plan
        opt = re.search(r'option\s*(\d+)', msg.lower())
        if opt and self.state.get('plans'):
            idx = int(opt.group(1)) - 1
            if 0 <= idx < len(self.state['plans']):
                self.state['selected_plan'] = self.state['plans'][idx]
                return {'selected_plan': self.state['selected_plan'], 'state': self.state}

        # confirm selection
        if msg.lower() == "confirm" and self.state.get("selected_plan"):
            plan = self.state["selected_plan"]
            return {
                "confirmation": f"You have confirmed the plan: {plan}. Redirecting to purchase...",
                "plan_payload": {
                    "plan": plan,
                    "user_id": "<session_token>"
                },
                "state": self.state
            }

        # cancel selection
        if msg.lower() == "cancel":
            self.state["selected_plan"] = None
            return {
                "prompt": "Okay, feel free to select another option.",
                "state": self.state
            }

        # LLM logic
        if self.agent_executor:
            try:
                result = self.agent_executor.invoke({'input': msg})
                self.state['last_response'] = result.get('output', '')
                return {'response': self.state['last_response'], 'state': self.state}
            except Exception as e:
                self._exception_handle(msg='LLM agent failed', exception=e, is_fatal=False)

        # fallback regex parsing
        return self._regex_step(msg)

    def _regex_step(self, msg: str) -> dict:
        dest_raw = self._parse_destination(msg)
        if dest_raw:
            self.state['destination'] = dest_raw

        dur = self._parse_duration(msg)
        if dur:
            self.state['duration_days'] = dur

        data_needed = self._parse_data_amount(msg)
        if data_needed is not None:
            self.state['data_needed_gb'] = data_needed

        service = self._parse_service_type(msg)
        if service:
            self.state['service_type'] = service

        if self.state['destination']:
            canonical = self._canonical_destination(self.state['destination'])
            if not canonical:
                err = f'no zone found for {self.state["destination"]}'
                self.state['plans'] = []
                return {'plans': [], 'error': err, 'state': self.state}
            self.state['destination'] = canonical

        if self.state['destination'] == '':
            return {'prompt': 'Which country will you visit?', 'state': self.state}
        if self.state['duration_days'] is None:
            return {'prompt': 'How long is your trip in days?', 'state': self.state}
        if self.state['service_type'] == 'data' and self.state['data_needed_gb'] is None:
            return {'prompt': 'How much data do you need in GB?', 'state': self.state}

        plans = self.recommender.recommend(
            destination=self.state['destination'],
            duration_days=self.state['duration_days'],
            service_type=self.state['service_type'],
            data_needed_gb=self.state['data_needed_gb'],
        )
        self.state['plans'] = plans
        if plans and 'error' in plans[0]:
            return {'plans': [], 'error': plans[0]['error'], 'state': self.state}
        return {'plans': plans, 'state': self.state}

    def _tool_recommend(self, destination: str, duration_days: int, service_type: str = "data", data_needed_gb: Optional[float] = None):
        # Simple input validation
        known_destinations = self.recommender.get_destinations()
        if destination.lower() not in known_destinations:
            return f"Sorry, '{destination}' is not a known travel destination. Could you clarify?"

        if duration_days < 1 or duration_days > 90:
            return f"That doesn't look like a valid trip duration. Please specify a trip between 1 and 90 days."

        if service_type == "data" and (data_needed_gb is None or data_needed_gb <= 0):
            return "Please specify how much data you expect to use, in GB."

        # Store in state
        self.state["destination"] = destination
        self.state["duration_days"] = duration_days
        self.state["service_type"] = service_type
        self.state["data_needed_gb"] = data_needed_gb

        plans = self.recommender.recommend(destination, duration_days, service_type, data_needed_gb)
        self.state["plans"] = plans

        if not plans or "error" in plans[0]:
            return plans[0].get("error", "No plans found.")

        lines = ["Here are your top recommended plans:"]
        for i, plan in enumerate(plans, 1):
            lines.append(
                f"{i}. {plan['data_gb']}GB for {plan['duration_days']} days at S${plan['price_sgd']:.2f} (Zone {plan['zone']})"
            )
        lines.append("\nPlease type 'Option 1', 'Option 2', etc. to select a plan.")
        return "\n".join(lines)
