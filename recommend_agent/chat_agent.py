from typing import Optional
import re
import pandas as pd
from base import BaseHandler
from .recommend import RoamingPlanRecommender


class RoamingPlanAgent(BaseHandler):
    """Lightweight conversational agent for roaming plan queries."""

    def __init__(self, recommender: RoamingPlanRecommender=None):
        self.recommender = recommender or RoamingPlanRecommender()
        # ensure database is available
        self.recommender.db_build()
        self._load_destinations()
        self.reset()
        super().__init__()

    def _load_destinations(self):
        try:
            df = pd.read_csv('data/destination.csv')
            self._dest_lookup = {c.lower(): c for c in df['country'].tolist()}
        except Exception:
            self._dest_lookup = {}

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

    # ------------------------------------------------------------------ parsing
    def _parse_destination(self, text: str) -> str:
        match = re.search(r'(?:to|in) ([A-Za-z ,\'\-]+)', text)
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

        # plan selection
        opt = re.search(r'option\s*(\d+)', msg.lower())
        if opt and self.state.get('plans'):
            idx = int(opt.group(1)) - 1
            if 0 <= idx < len(self.state['plans']):
                self.state['selected_plan'] = self.state['plans'][idx]
                return {'selected_plan': self.state['selected_plan']}

        if self.state['destination']:
            canonical = self._canonical_destination(self.state['destination'])
            if not canonical:
                err = f'no zone found for {self.state["destination"]}'
                self.state['plans'] = []
                return {'plans': [], 'error': err}
            self.state['destination'] = canonical

        # gather missing info prompts
        if self.state['destination'] is None:
            return {'prompt': 'Which country will you visit?'}
        if self.state['duration_days'] is None:
            return {'prompt': 'How long is your trip in days?'}
        if self.state['service_type'] == 'data' and self.state['data_needed_gb'] is None:
            return {'prompt': 'How much data do you need in GB?'}

        # ready to recommend
        plans = self.recommender.recommend(
            destination=self.state['destination'],
            duration_days=self.state['duration_days'],
            service_type=self.state['service_type'],
            data_needed_gb=self.state['data_needed_gb'],
        )
        self.state['plans'] = plans
        if plans and 'error' in plans[0]:
            return {'plans': [], 'error': plans[0]['error']}
        return {'plans': plans}

