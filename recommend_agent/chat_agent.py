# recommend_agent/tools.py
import pandas as pd
from langchain.tools import tool
from .recommend import RoamingPlanRecommender


@tool
def plans_db_tool(destination: str, duration: str = "1 day", service_type: str = "data") -> str:
    """
    Recommends the top 3 roaming plans for a given destination, duration, and service type.
    Accepts:
      - destination: country name
      - duration: pass duration (e.g., "1 day", "3 days")
      - service_type: one of "data", "calls", or "sms"
    Returns:
      - A summary of the top 3 matching plans with pros/cons.
    """
    try:
        candidates = df[df['Destination'].str.lower() == destination.lower()]
        candidates = candidates[candidates['Data_Pass_Validity'].str.lower() == duration.lower()]
        if candidates.empty:
            return f"No plans found for {destination} with duration {duration}."

        results = []
        for _, row in candidates.iterrows():
            score = 0
            if service_type == "data":
                score = float(row['Data_Pass_Data'].replace("GB", "").replace("MB", ""))
            elif service_type == "calls":
                score = -float(row['Pay_Per_Use_Call_Outgoing'].replace("S$", "").split("/")[0])
            elif service_type == "sms":
                score = -float(row['Pay_Per_Use_SMS'].replace("S$", "").split("/")[0])

            results.append((score, row))

        top3 = sorted(results, key=lambda x: -x[0])[:3]
        response = ""
        for i, (_, plan) in enumerate(top3, 1):
            response += (
                f"\n{i}. Zone: {plan['Zone']}, Destination: {plan['Destination']}, "
                f"Price: {plan['Data_Pass_Price']}, Data: {plan['Data_Pass_Data']}, "
                f"Calls: {plan['Pay_Per_Use_Call_Outgoing']}, SMS: {plan['Pay_Per_Use_SMS']}"
            )
        return response.strip()
    except Exception as e:
        return f"Error processing request: {str(e)}"
