#!/usr/bin/env python3
"""roaming plan recommendation tool that selects best match plan from roaming plans database based on user features

RoamingPlanRecommender.recommend()

  - takes inputs
    - destination: location 
    - trip duration: number of days
    - service type: [data, sms, calls]
    - data needed: amount of data needed in GB

  - returns results as a JSON row from the roaming plan database
    {
        "zone": <geographic category Zone 1 through 3>,
        "duration_days": <duration of trip in days>,
        "data_gb": <plan GB>,
        "price_sgd": <plan price $>,
        "rate_data_per_10kb": <rate $ per 10 KB above plan GB>,
        "rate_calls_outgoing_per_min": <rate $ per min>,
        "rate_calls_incoming_per_min": <rate $ per min>,
        "rate_per_sms": <rate $ per SMS>
    }
"""
# dependencies -------------------------------------------------------------------------------------------------------
from typing import Optional
from .roaming_plans import DBConnector
from base import BaseHandler


# constants -------------------------------------------------------------------------------------------------------
SHORTLIST_NUM_DEFAULT = 3
LARGE_GB = 1000
SERVICE_TYPES = [
    'data',
    'calls',
    'sms'
]

# module variables -------------------------------------------------------------------------------------------------


# classes ------------------------------------------------------------------------------------------------------------
class RoamingPlanRecommender(BaseHandler):
    def __init__(self, shortlist_num=None):
        self.db = DBConnector()
        self.recommend_shortlist_num: int = shortlist_num or SHORTLIST_NUM_DEFAULT
        super().__init__()

    def __repr__(self):
        return f'<{self.__class__.__name__}: [{self.status()}]>'

    def status(self):
        self._status_update_from_db()
        return super().status()

    def _status_update_from_db(self):
        if self.db.status() == 'ERROR':
            self._status_code = 2
            self.error = f'{self.error} database error {self.db.error}'
        elif self.db.status() == 'READY' and self._status_code == 1:
            self._status_code = 0

    def db_build(self):
        build_success = self.db.build()
        if not build_success:  
            ex_msg = f'failed to build roaming plans database. {self.db.error}'          
            self._exception_handle(msg=ex_msg)
        return build_success

    def exit(self):
        close_success = self.db_close()
        self.db = None

    def db_close(self):
        if self.db:
            self.db.close()
        return True

    def db_connect(self):
        if self.db is None:
            self.db = DBConnector()
        if self.db.connected():
            return True
        else:
            self.db.connect()
            if self.db.connected():
                return True
            else:
                ex_msg = f'failed to connect to database. {self.db.error}'
                self._exception_handle(msg=ex_msg)
                return False

    def recommend(
        self,
        destination: str,
        duration_days: int,
        service_type: str = "data",
        data_needed_gb: float = None
    ) -> list[dict]:

        if not self.db_connect():
            ex_msg = f'problem connecting to roaming plan database {self.db.error}'
            self._exception_handle(msg=ex_msg)
            return [{'error': ex_msg}]

        try:
            zone = self._get_zone_from_destination(destination)
            if zone is None:
                ex_msg = f'ERROR. no zone found for {destination}'
                self._exception_handle(msg=ex_msg)
                return [{'error': ex_msg}]


            plans = self._get_all_plans_for_zone(zone)
            if not plans:
                ex_msg = f'ERROR. no plans found for zone {zone}'
                self._exception_handle(msg=ex_msg)
                return [{'error': ex_msg}]

            rates = self._get_rates_for_zone(zone)
            if not rates:
                ex_msg = f'ERROR. no rates found for zone {zone}'
                self._exception_handle(msg=ex_msg)
                return [{'error': ex_msg}]

            # exact match
            exact_plans = [p for p in plans if p['duration_days'] == duration_days]
            candidates = exact_plans

            if not exact_plans:
                interpolated = self._interpolate_plan(plans, duration_days, zone)
                if interpolated:
                    candidates = [interpolated]

            if not candidates:
                candidates = plans

            score_results = [
                (self._score_plan(p, zone, service_type, data_needed_gb), p)
                for p in candidates
            ]
            results = [r for r in score_results if r[0] is not None]

            results_sorted = sorted(results, key=lambda x: -x[0])[:self.recommend_shortlist_num]
            top_plans = [r[1] for r in results_sorted]

            add_rates = [{**{k: v for k, v in p.items() if k != 'id'}, **rates} for p in top_plans]
            return add_rates

        except Exception as e:
            ex_msg = f'Recommendation query failed: {e}'
            self._exception_handle(msg=ex_msg, exception=e)
            return [{'error': ex_msg}]

    def _get_zone_from_destination(self, country: str) -> Optional[int]:
        self.db.execute("SELECT zone FROM destination WHERE lower(country) = ?", args=(country.lower(),))
        result = self.db.cursor.fetchone()
        return result[0] if result else None

    def _get_rates_for_zone(self, zone: int) -> list[dict]:
        self.db.execute("SELECT rate_data_per_10kb, rate_calls_outgoing_per_min, rate_calls_incoming_per_min, rate_per_sms FROM ppu_rate WHERE zone = ?", args=(zone,))
        columns = [desc[0] for desc in self.db.cursor.description]
        result = self.db.cursor.fetchone()
        rates = dict(zip(columns, result)) if result else {}
        return rates

    def _get_all_plans_for_zone(self, zone: int) -> list[dict]:
        self.db.execute("SELECT * FROM plan WHERE zone = ?", args=(zone,))
        columns = [desc[0] for desc in self.db.cursor.description]
        plans = [dict(zip(columns, row)) for row in self.db.cursor.fetchall()]
        return plans

    def _interpolate_plan(self, plans: list[dict], duration: int, zone: int) -> Optional[dict]:
        lower = [p for p in plans if p['duration_days'] < duration]
        upper = [p for p in plans if p['duration_days'] > duration]

        if not lower or not upper:
            return None

        p_low = max(lower, key=lambda x: x['duration_days'])
        p_high = min(upper, key=lambda x: x['duration_days'])

        def interp(field):
            x0, y0 = p_low['duration_days'], p_low[field]
            x1, y1 = p_high['duration_days'], p_high[field]
            return round(y0 + ((duration - x0) / (x1 - x0)) * (y1 - y0), 2)

        return {
            'zone': zone,
            'duration_days': duration,
            'data_gb': interp('data_gb'),
            'price_sgd': interp('price_sgd'),
            'id': -1  # synthetic
        }

    def _score_plan(self, plan: dict, zone: int, service: str, data_needed: float) -> Optional[float]:
        if service == "data":
            return plan['data_gb']
        
        elif service == "calls":
            self.db.execute("SELECT rate_calls_outgoing_per_min FROM ppu_rate WHERE zone = ?", (zone,))
            return -self.db.cursor.fetchone()[0]
        
        elif service == "sms":
            self.db.execute("SELECT rate_per_sms FROM ppu_rate WHERE zone = ?", (zone,))
            return -float(self.db.cursor.fetchone()[0])
        
        elif service not in SERVICE_TYPES:
            msg = f'unsupported service type: {service}. Allowed {SERVICE_TYPES}'
            raise ValueError(msg)
        
        return None