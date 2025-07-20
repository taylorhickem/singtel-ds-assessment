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
        "Zone": <geographic category Zone 1 through 3>,
        "Destination": <geographic destination ex Malaysia>,
        "Data_Pass_Validity": <duration of trip in days>,
        "Data_Pass_Data": <data amount in GB>,
        "Data_Pass_Price": <data plan price in SGD>
    }
"""
# dependencies -------------------------------------------------------------------------------------------------------
import pandas as pd
from .roaming_plans import DBConnector


# constants -------------------------------------------------------------------------------------------------------


# module variables -------------------------------------------------------------------------------------------------
plans = None


# helper functions -------------------------------------------------------------------------------------------------
def duration_to_days(duration_str: str) -> int:
    return int(duration_str.lower().replace("days", "").replace("day", "").strip())


# classes ------------------------------------------------------------------------------------------------------------
class RoamingPlanRecommender:
    def __init__(self):
        self.db = DBConnector()

    def db_build(self):
        build_success = self.db.build()
        if not build_success:  
            ex_msg = f'failed to build roaming plans database. {self.db.error}'          
            raise RuntimeError(ex_msg)

    def recommend(
        self,
        destination: str,
        duration: str,
        service_type: str = "data",
        data_needed_gb: float = None
    ) -> list[dict]:
        # Step 1: Filter by destination and duration
        candidates = plans[
            (plans['Destination'].str.lower() == destination.lower()) &
            (plans['Data_Pass_Validity'].str.lower() == duration.lower())
        ]

        if candidates.empty:
            return []

        results = []

        # Step 2: Score based on service type and data requirement
        for _, row in candidates.iterrows():
            score = 0
            try:
                if service_type == "data":
                    plan_gb = float(row['Data_Pass_Data'].replace("GB", "").replace("MB", ""))

                    # Reject plans that offer less than required data
                    if data_needed_gb is not None and plan_gb < data_needed_gb:
                        continue

                    score = plan_gb  # simple scoring by GB offered

                elif service_type == "calls":
                    cost_per_min = float(row['Pay_Per_Use_Call_Outgoing'].replace("S$", "").split("/")[0])
                    score = -cost_per_min

                elif service_type == "sms":
                    cost_per_sms = float(row['Pay_Per_Use_SMS'].replace("S$", "").split("/")[0])
                    score = -cost_per_sms

                results.append((score, row.to_dict()))

            except (ValueError, AttributeError):
                continue  # Skip row if conversion fails

        if not results:
            return []

        # Step 3: Sort and return top 3
        top3 = sorted(results, key=lambda x: -x[0])[:3]
        return [entry[1] for entry in top3]


# roaming plan db ---------------------------------------------------------------------------------------
def db_create_from_csv_files():
    pass

def plans_db_load(csv_path=ROAMING_PLAN_CSV_FILE):
    global plans
    plans = pd.read_csv(csv_path)


